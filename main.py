from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import build.blockchain as bc

app = FastAPI(title="Supply‑Chain‑Blockchain API")

# ──────────────────────────────────────────────
#  3.1  initialise chain & helpers
# ──────────────────────────────────────────────
CHAIN = bc.Blockchain(3)     # difficulty 3 → fast demo
WORLD_STATE = {}             # asset_id → current_owner

def append_block(transactions):
    """transactions: list[bc.Transaction]"""
    CHAIN.add_block(transactions)
    refresh_state()

def refresh_state():
    WORLD_STATE.clear()
    for block in CHAIN.get_blocks():
        for tx in block:
            # tx format "Alice->Bob: 0.000000"
            sender, rest = tx.split("->")
            receiver, _ = rest.split(":")
            asset = _.strip()                      # asset id encoded in 'amount'
            WORLD_STATE[asset] = receiver.strip()

refresh_state()

# ──────────────────────────────────────────────
#  3.2  request models
# ──────────────────────────────────────────────
class CreateAssetBody(BaseModel):
    asset_id: str
    owner: str

class TransferBody(BaseModel):
    asset_id: str
    new_owner: str

# ──────────────────────────────────────────────
#  3.3  endpoints
# ──────────────────────────────────────────────
@app.post("/asset")
def create_asset(body: CreateAssetBody):
    if body.asset_id in WORLD_STATE:
        raise HTTPException(400, "Asset already exists")
    tx = bc.Transaction("GENESIS", body.owner, float(body.asset_id))
    append_block([tx])
    return {"status": "created", "chain_height": len(CHAIN.get_blocks())}

@app.post("/transfer")
def transfer_asset(body: TransferBody):
    owner = WORLD_STATE.get(body.asset_id)
    if not owner:
        raise HTTPException(404, "Asset not found")
    tx = bc.Transaction(owner, body.new_owner, float(body.asset_id))
    append_block([tx])
    return {"status": "transferred", "from": owner, "to": body.new_owner}

@app.get("/asset/{asset_id}")
def asset_history(asset_id: str):
    history = []
    for height, block in enumerate(CHAIN.get_blocks()):
        for tx in block:
            if f": {asset_id}" in tx:
                history.append({"block": height, "tx": tx})
    if not history:
        raise HTTPException(404, "Not found")
    return {"latest_owner": WORLD_STATE[asset_id], "history": history}

@app.get("/chain")
def get_chain():
    return CHAIN.get_blocks()

