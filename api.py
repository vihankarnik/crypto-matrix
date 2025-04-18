import os, requests, sys
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import build.blockchain as bc

from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="SupplyChain Node")
# Allow any origin / method for P2P & UI calls
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# ─── Peer Identity ──────────────────────────────────────────
SELF_PORT     = int(os.getenv("SELF_PORT", "8001"))
SELF_URL      = f"http://127.0.0.1:{SELF_PORT}"
BOOTSTRAP_URL = os.getenv("BOOTSTRAP_URL")        # e.g. "http://localhost:8001"
PEERS         = set()
CHAIN         = bc.Blockchain(3)
WORLD_STATE   = {}
INVENTORY     = {}

# ─── Data Models ────────────────────────────────────────────
class TxModel(BaseModel):
    event:     str    # "CREATE" or "TRANSFER"
    asset_id:  str
    from_party:str = ""
    to_party:  str
    meta:      str = ""

class PeerModel(BaseModel):
    peer_url: str

# ─── Lifecycle Hooks ────────────────────────────────────────
@app.on_event("startup")
def startup():
    # 1) register self
    PEERS.add(SELF_URL)

    # 2) join bootstrap (if provided)
    if BOOTSTRAP_URL and BOOTSTRAP_URL != SELF_URL:
        try:
            # tell bootstrap about us
            requests.post(f"{BOOTSTRAP_URL}/peers",
                          json={"peer_url": SELF_URL}, timeout=2)
            # fetch their peer list
            res = requests.get(f"{BOOTSTRAP_URL}/peers", timeout=2)
            if res.ok:
                for p in res.json():
                    PEERS.add(p)
            # ensure bootstrap is known
            PEERS.add(BOOTSTRAP_URL)
            print(PEERS)
        except Exception as e:
            print("⚠ Bootstrap join failed:", e)

    # 3) sync chain from first reachable peer
    sync_chain()

    # 4) build world state for quick lookups
    refresh_state()


# ─── Helper Functions ───────────────────────────────────────
def get_internal_ip() -> str | None:
    """Get the *local* IP address of the current machine.

    From: https://stackoverflow.com/a/28950776

    Returns
    -------
    string
        The local IPv4 address of the current machine.

    """
    import socket

    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        try:
            # Doesn't even have to be reachable
            s.connect(("8.8.8.8", 1))
            _internal_ip = s.getsockname()[0]
        except Exception:
            _internal_ip = "127.0.0.1"

    return _internal_ip

print("Private IP:", get_internal_ip())
print("heyyy")

def sync_chain():
    for peer in list(PEERS):
        if peer == SELF_URL:
            continue
        try:
            r = requests.get(f"{peer}/chain", timeout=2)
            if r.ok:
                CHAIN.load_chain(r.json())
                print(f"🔄 Synced chain from {peer}")
                return
        except Exception as e:
            print(f"⚠ Chain sync failed from {peer}: {e}")

def refresh_state():
    """
    Re‑build WORLD_STATE and INVENTORY from scratch.
    If any mismatch is found (e.g., an asset appears twice) we raise.
    """
    WORLD_STATE.clear()
    INVENTORY.clear()

    for block in CHAIN.get_blocks():
        for tx in block:
            parts = tx.split()
            # "[CREATE] SKU GENESIS -> Alice | ... "
            if len(parts) < 4:
                continue
            aid = parts[1]
            owner = parts[3]

            # ------------- 1) check duplicates -------------
            if aid in WORLD_STATE and WORLD_STATE[aid] == owner:
                raise ValueError(f"Duplicate CREATE or invalid transfer for asset {aid}")

            # ------------- 2) update state / inventory -----
            WORLD_STATE[aid] = owner
            if owner not in INVENTORY:
                INVENTORY[owner] = set()
            INVENTORY[owner].add(aid)

def broadcast(tx_data):
    for peer in list(PEERS):
        if peer == SELF_URL:
            continue
        try:
            requests.post(f"{peer}/receive", json=tx_data, timeout=1)
        except:
            pass

@app.get("/inventory")
def inventory():
    # convert set -> list for JSON serialisation
    return {owner: list(ids) for owner, ids in INVENTORY.items()}

# ─── P2P Peer Endpoints ─────────────────────────────────────
@app.post("/peers")
def register_peer(peer: PeerModel):
    PEERS.add(peer.peer_url)
    return {"peers": list(PEERS)}

@app.get("/peers")
def get_peers():
    return list(PEERS)

# ─── Blockchain Endpoints ───────────────────────────────────
@app.post("/asset")
def create_asset(tx: TxModel):
    if tx.asset_id in WORLD_STATE:
        raise HTTPException(400, "Asset already exists")
    t = bc.Transaction.create(tx.asset_id, tx.to_party, tx.meta)
    CHAIN.add_block([t])
    refresh_state()
    broadcast(tx.dict())
    return {"status": "created"}

@app.post("/transfer")
def transfer_asset(tx: TxModel):
    # 1) asset must exist
    current_owner = WORLD_STATE.get(tx.asset_id)
    if current_owner is None:
        raise HTTPException(404, "Asset not found")

    # 2) only the real owner can transfer
    if tx.from_party != current_owner:
        raise HTTPException(400,
            f"Transfer failed: asset '{tx.asset_id}' is owned by '{current_owner}', not '{tx.from_party}'"
        )

    # 3) everything ok → create tx
    t = bc.Transaction.transfer(tx.asset_id, tx.from_party, tx.to_party, tx.meta)
    CHAIN.add_block([t])
    refresh_state()
    broadcast(tx.dict())
    return {"status": "transferred", "from": tx.from_party, "to": tx.to_party}

@app.post("/receive")
def receive_from_peer(tx: TxModel):
    t = bc.Transaction.create(tx.asset_id, tx.to_party, tx.meta) \
        if tx.event == "CREATE" \
        else bc.Transaction.transfer(tx.asset_id, tx.from_party, tx.to_party, tx.meta)
    CHAIN.add_block([t])
    refresh_state()
    return {"status": "accepted"}

@app.get("/chain")
def get_chain():
    return CHAIN.get_blocks()

@app.get("/chain_full")
def chain_full():
    """
    Returns every block with real nonce, prev‐hash, block‐hash, and tx list.
    """
    return CHAIN.get_chain_full()


@app.get("/state")
def get_state():
    return WORLD_STATE
