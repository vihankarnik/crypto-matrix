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
            .hblk h4{
                margin:0 0 8px 0;
                font-weight:600;
                color:#fff;
                font-size: 1rem;
            }
            .tx{
                font-family:monospace;
                font-size:0.8rem;
                background:#052e16;
                color:#d1fae5;
                padding:2px 6px;
                border-radius:4px;
                display:inline-block;
                margin:2px 2px 4px 0;
            }
            .arrowbox {
                font-size: 2rem;
                text-align: center;
                padding-top: 36px;
                color: #888;
            }
        </style>
        """,
        unsafe_allow_html=True,
    )

    # ---------- 2. horizontal chain layout ----------
    blocks = main.get_blocks()

    # Batch blocks in groups of 4 to avoid overflowing width
    max_per_row = 4
    for start in range(0, len(blocks), max_per_row):
        row_blocks = blocks[start:start + max_per_row]
        cols = st.columns(len(row_blocks) * 2 - 1)

        for idx, txs in enumerate(row_blocks):
            col_idx = idx * 2
            with cols[col_idx]:
                st.markdown(
                    f"""
                    <div class="hblk">
                        <h4>🔗 Block&nbsp;{start + idx + 1}</h4>
                        {"".join(f'<div class="tx">{tx}</div>' for tx in txs)}
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

            # Add ➜ arrow between blocks
            if idx != len(row_blocks) - 1:
                with cols[col_idx + 1]:
                    st.markdown('<div class="arrowbox">➜</div>', unsafe_allow_html=True)
