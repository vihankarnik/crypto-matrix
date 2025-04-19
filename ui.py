import streamlit as st
import os, requests

API_PORT = os.getenv('SELF_PORT', '8001')
API = f"http://127.0.0.1:{API_PORT}"
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
            try:
                res = requests.post(f"{API}/asset", json={"event": ev, "asset_id": aid, "to_party": to, "meta": meta})
                st.success(f"✅ Success! {res.json()}")
            except requests.exceptions.RequestException as e:
                st.error(f"❌ Request failed: {e}")
    else:
        frm = st.text_input("From")
        to  = st.text_input("To")
        if st.button("Transfer"):
            try:
                res = requests.post(f"{API}/transfer", json={"event": ev, "asset_id": aid, "from_party": frm, "to_party": to, "meta": meta})
                st.success(f"✅ Success! {res.json()}")
            except requests.exceptions.RequestException as e:
                st.error(f"❌ Request failed: {e}")

with tab2:
    # ---------- 1. one-time CSS ----------
    st.markdown(
        """
        <style>
            .hblk {
                background:#111;
                border:1px solid #333;
                border-radius:10px;
                padding:12px;
                min-width: 200px;
                min-height: 100px;
                text-align: left;
            }
            .arrowbox {
                font-size: 2rem;
                padding-top: 8rem;
                display: flex;
                justify-content: center;    /* horizontally center */
                align-items: center;        /* vertically center */
                height: 100%;
                color: #888;
            }
        </style>
        """,
        unsafe_allow_html=True,
    )
    st.header("Blockchain Ledger")

    # fetch rich chain data
    data = []
    try:
        res = requests.get(f"{API}/chain_full")
        if res.ok:
            data = res.json()
    except requests.exceptions.RequestException as e:
        st.error(f"❌ Request failed: {e}")

    max_per_row = 3
    for i in range(0, len(data), max_per_row):
        # cols = st.columns(max_per_row*2 )
        cols = st.columns([6, 1] * (max_per_row ))
        for j, blk in enumerate(data[i:i+max_per_row]):
            j = j*2     # to account for the arrow
            with cols[j]:
                st.markdown(f"""
                    <div class='hblk'>
                        <h3>Block #{blk['index']}</h3>
                        <p><strong>Nonce:</strong> {blk['nonce']}<br>
                        <strong>Prev:</strong> <code>{blk['prev']}</code><br>
                        <strong>Hash:</strong> <code>{blk['hash']}</code><br>
                        <strong>Tx Count:</strong> {len(blk['tx'])}</p>
                    </div>
                """, unsafe_allow_html=True)
                for tx in blk["tx"]:
                    st.code(tx)
            # adding arrow
            if i != len(data) - 1:
                with cols[j + 1]:
                    st.markdown('<div class="arrowbox">➜</div>', unsafe_allow_html=True)



with tab3:
    st.header("World State")
    try:
        res = requests.get(f"{API}/state")
        if res.ok:
            state = res.json()
            st.json(state)
    except requests.exceptions.RequestException as e:
        st.error(f"❌ Request failed: {e}")
