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
    cols = st.columns(4)
    blocks = requests.get(f"{API}/chain").json()
    for i, blk in enumerate(blocks, start=1):
        col = cols[(i-1)%4]
        with col:
            st.markdown(f"*Block {i}*")
            for tx in blk:
                st.code(tx)
            if i < len(blocks): st.markdown("➜")

with tab3:
    st.header("World State")
    state = requests.get(f"{API}/state").json()
    st.json(state)
