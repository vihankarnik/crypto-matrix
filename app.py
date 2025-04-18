# app.py
import streamlit as st
import main  # uses create_asset, transfer_asset, get_blocks

st.set_page_config(page_title="Supply Chain Blockchain", layout="wide")
st.title("📦 Supply Chain Blockchain Explorer")

# ─── Tabs for interaction ─────────────────────────────
tab1, tab2 = st.tabs(["➕ Add Transaction", "🔗 View Blockchain"])

with tab1:
    tx_type = st.radio("Transaction Type", ["Create", "Transfer"])
    asset_id = st.text_input("Asset ID", placeholder="e.g., SKU-123")
    meta = st.text_area("Meta / Notes", placeholder="Any extra info...")

    if tx_type == "Create":
        owner = st.text_input("Owner")
        if st.button("Create Asset"):
            if asset_id and owner:
                main.create_asset(asset_id, owner, meta)
                st.success(f"Created asset '{asset_id}' owned by {owner}")
            else:
                st.error("Asset ID and Owner are required.")
    else:
        from_party = st.text_input("From")
        to_party = st.text_input("To")
        if st.button("Transfer Asset"):
            if asset_id and from_party and to_party:
                main.transfer_asset(asset_id, from_party, to_party, meta)
                st.success(f"Transferred '{asset_id}' from {from_party} to {to_party}")
            else:
                st.error("Asset ID, From, and To are required.")

with tab2:
    blocks = main.get_blocks()
    for i, txs in enumerate(blocks):
        with st.expander(f"🔗 Block {i} — {len(txs)} transactions"):
            for tx in txs:
                st.markdown(f"- `{tx}`")
