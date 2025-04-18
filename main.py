# main.py
import build.blockchain as bc

# Initialize the blockchain
chain = bc.Blockchain()

# Convenience functions
def create_asset(asset_id, owner, meta=""):
    tx = bc.Transaction.create(asset_id, owner, meta)
    chain.add_block([tx])

def transfer_asset(asset_id, from_party, to_party, meta=""):
    tx = bc.Transaction.transfer(asset_id, from_party, to_party, meta)
    chain.add_block([tx])

def get_blocks():
    return chain.get_blocks()
