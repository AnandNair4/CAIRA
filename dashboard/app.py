"""CAIRA SOC dashboard.

Talks to the FastAPI service (api/app.py) via HTTP instead of touching
the database directly.
"""

import requests
import streamlit as st

API_BASE = st.sidebar.text_input("API base URL", value="http://localhost:8000")

st.set_page_config(page_title="CAIRA SOC Dashboard", layout="wide")
st.title("CAIRA SOC Dashboard")


def fetch(path: str) -> dict | None:
    try:
        resp = requests.get(f"{API_BASE}{path}", timeout=10)
        resp.raise_for_status()
        return resp.json()
    except requests.RequestException as exc:
        st.error(f"API request failed: {exc}")
        return None


tab_logs, tab_intel, tab_assets = st.tabs(["Log Lookup", "Threat Intel", "Asset Criticality"])

with tab_logs:
    user = st.text_input("User", value="jdoe", key="log_user")
    if st.button("Fetch logs", key="fetch_logs"):
        st.json(fetch(f"/logs/{user}"))

with tab_intel:
    ip = st.text_input("IP address", value="203.0.113.5", key="intel_ip")
    if st.button("Check intel", key="fetch_intel"):
        st.json(fetch(f"/intel/{ip}"))

with tab_assets:
    asset_user = st.text_input("User", value="admin_user", key="asset_user")
    if st.button("Fetch criticality", key="fetch_assets"):
        st.json(fetch(f"/assets/{asset_user}"))
