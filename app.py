import streamlit as st
import pandas as pd
import numpy as np

# Page Configuration
st.set_page_config(
    page_title="HEXAKADAL - Ocean Freight Engine",
    page_icon="⚓",
    layout="wide"
)

# Title & Header
st.title("⚓ HEXAKADAL")
st.subheader("AI-Based Ocean Freight Engine for Bulk Cargo Procurement to India's East Coast")
st.caption("Commercial Decision Support System for Chartering Managers & Port Operations (Values in USD)")

# Sidebar Inputs
st.sidebar.header("🚢 Voyage & Cargo Parameters")

vessel_list = [
    "MV ORE BRASIL (400k DWT Valemax)",
    "MV CAPESIZE HERO (180k DWT Capesize)",
    "MV PANAMAX STAR (75k DWT Panamax)",
    "MV SUPRAMAX OCEAN (55k DWT Supramax)"
]
selected_vessel = st.sidebar.selectbox("Select Vessel", vessel_list)

cargo_qty = st.sidebar.number_input("Cargo Quantity (Metric Tons)", min_value=10000, max_value=500000, value=150000, step=5000)
demurrage_rate = st.sidebar.number_input("Daily Demurrage Rate ($ USD / day)", min_value=5000.0, max_value=100000.0, value=30000.0, step=1000.0)

origin_port = st.sidebar.selectbox("Origin Port", ["Hay Point (Australia)", "Newcastle (Australia)", "Saldanha Bay (South Africa)", "Port Hedland (Australia)"])
destination_port = st.sidebar.selectbox("Destination Port (India)", ["Paradip Port", "Visakhapatnam Port", "Haldia Port", "Dhamra Port", "Gopalpur Port"])

# --- PORT DRAFT DATABASE & AUTO-FETCH LOGIC ---
port_draft_database = {
    "Paradip Port": 17.50,
    "Visakhapatnam Port": 16.10,
    "Haldia Port": 8.50,
    "Dhamra Port": 18.00,
    "Gopalpur Port": 14.50
}

# Automatically fetch port draft depth based on selected destination port
auto_max_draft = port_draft_database.get(destination_port, 15.00)

st.sidebar.markdown("---")
st.sidebar.header("🚆 Vessel & Port Operations")
st.sidebar.info(f"**Auto-Fetched Max Draft for {destination_port}:** `{auto_max_draft} meters`")

vessel_draft_input = st.sidebar.slider(
    "Vessel Draft Depth (Meters)",
    min_value=5.0,
    max_value=25.0,
    value=float(auto_max_draft),
    help="Automatically dynamically set to destination port max draft depth limit."
)

# Calculations & Logic Engine
current_rate = 18.50  # USD/MT
predicted_rate = 16.28 # USD/MT

rate_savings = (current_rate - predicted_rate) * cargo_qty
tidal_delay_hours = 25.7
demurrage_loss = (demurrage_rate / 24.0) * tidal_delay_hours
ndv = rate_savings - demurrage_loss

# Action Signal Banner
if ndv > 0:
    st.error("🔥 **EXECUTIVE ACTION SIGNAL: WAIT / DEFER FIXING**")
    st.info(f"💡 **Explainable AI (XAI) Rationale:** Rate forecasted to drop from ${current_rate}/MT to ${predicted_rate}/MT. Expected Net Savings after Demurrage: ${ndv:,.2f}.")
else:
    st.success("✅ **EXECUTIVE ACTION SIGNAL: FIX IMMEDIATELY**")
    st.info("💡 **Explainable AI (XAI) Rationale:** Freight rates expected to increase. Lock charterparty immediately to minimize demurrage exposure.")

# Display Financial Key Metrics
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Net Decision Value (NDV in USD)", f"${ndv:,.1f}")

with col2:
    st.metric("Potential Freight Savings (USD)", f"${rate_savings:,.1f}")

with col3:
    st.metric("Demurrage Loss Risk (USD)", f"${demurrage_loss:,.1f}")

with col4:
    st.metric("Total Congestion Queue", f"{tidal_delay_hours} Hours")

# Draft & Congestion Module Info
st.markdown("---")
c1, c2, c3 = st.columns(3)

with c1:
    st.markdown("### 📊 Module 1: Rate Forecaster")
    st.write(f"**Current Freight Rate:** ${current_rate} / MT")
    st.write(f"**7-Day AI Target Rate:** ${predicted_rate} / MT")

with c2:
    st.markdown("### 🚢 Module 2: Draft & Vessel Clearance")
    st.write(f"**Vessel Draft:** {vessel_draft_input} m")
    st.write(f"**{destination_port} Depth Limit:** {auto_max_draft} m")
    if vessel_draft_input <= auto_max_draft:
        st.success("✅ Safe Draft Clearance")
    else:
        st.error("❌ CRITICAL: Draft Limit Violation!")

with c3:
    st.markdown("### 🌊 Module 3: Live Weather & Congestion")
    st.write("**Live Ocean Wave Height:** 2.4 m")
    st.write("**Weather Status:** Moderate Swell")
    st.write(f"**Tidal Window Delay:** +{tidal_delay_hours} Hours")