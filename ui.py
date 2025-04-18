import streamlit as st
import os, requests

API = f"http://localhost:{os.getenv('PORT', '8001')}"
st.set_page_config(page_title="SCM Node", layout="wide")
st.title("📦 SupplyChain Node")

tab1, tab2, tab3 = st.tabs(["➕ Transact", "🔗 Chain", "🗺 State"])

with tab1:
    ev = st.radio("Event", ["CREATE", "TRANSFER"])
    aid = st.text_input("Asset ID")
    meta = st.text_area("Meta / Notes")
    if ev == "CREATE":
        to = st.text_input("Owner")
        if st.button("Create"):
            res = requests.post(f"{API}/asset", json={"event": ev, "asset_id": aid, "to_party": to, "meta": meta})
            st.success(res.json())
    else:
        frm = st.text_input("From")
        to  = st.text_input("To")
        if st.button("Transfer"):
            res = requests.post(f"{API}/transfer", json={"event": ev, "asset_id": aid, "from_party": frm, "to_party": to, "meta": meta})
            st.success(res.json())

with tab2:
    st.header("Blockchain Ledger")

    # fetch rich chain data
    data = requests.get(f"{API}/chain_full").json()

    # skip genesis?
    data = [b for b in data if b["index"] != 0]

    for i in range(0, len(data), 2):
        cols = st.columns(2)
        for j, blk in enumerate(data[i:i+2]):
            with cols[j]:
                st.markdown(f"### Block #{blk['index']}")
                st.markdown(f"- **Nonce:** {blk['nonce']}")
                st.markdown(f"- **Prev:** `{blk['prev']}`")
                st.markdown(f"- **Hash:** `{blk['hash']}`")
                st.markdown(f"- **Tx Count:** {len(blk['tx'])}")
                for tx in blk["tx"]:
                    st.code(tx)
        if i+2 < len(data):
            st.markdown("➜", unsafe_allow_html=True)



with tab3:
    st.header("World State")
    state = requests.get(f"{API}/state").json()
    st.json(state)
