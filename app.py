import streamlit as st
import requests
API = "http://localhost:8000"

st.set_page_config(page_title="SCM‑Chain Demo", layout="wide")
tabs = st.tabs(["Create Asset", "Transfer Asset", "Track Asset", "Blockchain"])

# ──────────────────────────────────────────────────
with tabs[0]:
    st.header("📦 Register new asset")
    asset = st.text_input("Asset ID (numeric for demo)")
    owner = st.text_input("Initial owner")
    if st.button("Create") and asset and owner:
        r = requests.post(f"{API}/asset", json={"asset_id": asset, "owner": owner})
        st.write(r.json() if r.ok else r.text)

# ──────────────────────────────────────────────────
with tabs[1]:
    st.header("🔄 Transfer asset")
    asset_t = st.text_input("Asset ID to transfer")
    new_owner = st.text_input("New owner name")
    if st.button("Transfer") and asset_t and new_owner:
        r = requests.post(f"{API}/transfer",
                          json={"asset_id": asset_t, "new_owner": new_owner})
        st.write(r.json() if r.ok else r.text)

# ──────────────────────────────────────────────────
with tabs[2]:
    st.header("🔍 Track asset")
    aid = st.text_input("Asset ID to track")
    if st.button("Get history") and aid:
        r = requests.get(f"{API}/asset/{aid}")
        if r.ok:
            st.success(f"Current owner: {r.json()['latest_owner']}")
            st.write(r.json()["history"])
        else:
            st.error(r.text)

# ──────────────────────────────────────────────────
with tabs[3]:
    st.header("⛓️  Raw blockchain")
    r = requests.get(f"{API}/chain")
    for i, block in enumerate(r.json()):
        st.subheader(f"Block {i}")
        for tx in block:
            st.code(tx, language="text")

