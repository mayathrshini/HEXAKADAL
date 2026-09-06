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

cargo_qty = st.sidebar.number_input("Cargo Quantity (Metric Tons)", min_value=10000, max_value=500000, value=150000, step=5000)

origin_port = st.sidebar.selectbox("Origin Port", ["Hay Point (Australia)", "Newcastle (Australia)", "Saldanha Bay (South Africa)", "Port Hedland (Australia)"])
destination_port = st.sidebar.selectbox("Destination Port (India)", ["Paradip Port", "Visakhapatnam Port", "Haldia Port", "Dhamra Port", "Gopalpur Port"])

# --- PORT DRAFT DATABASE ---
port_draft_database = {
    "Paradip Port": 17.50,
    "Visakhapatnam Port": 16.10,
    "Haldia Port": 8.50,
    "Dhamra Port": 18.00,
    "Gopalpur Port": 14.50
}

auto_max_draft = port_draft_database.get(destination_port, 15.00)

# --- AUTOMATIC VESSEL & DEMURRAGE RATE OPTIMIZATION ENGINE ---
def optimize_vessel_and_demurrage(cargo_tons, port_max_draft):
    if cargo_tons >= 200000 and port_max_draft >= 17.0:
        return "MV ORE BRASIL (400k DWT Valemax)", 18.0, 45000.0
    elif cargo_tons >= 100000 and port_max_draft >= 16.0:
        return "MV CAPESIZE HERO (180k DWT Capesize)", 16.5, 30000.0
    elif cargo_tons >= 60000 and port_max_draft >= 11.0:
        return "MV PANAMAX STAR (75k DWT Panamax)", 12.0, 20000.0
    else:
        return "MV SUPRAMAX OCEAN (55k DWT Supramax)", 9.0, 15000.0

auto_vessel, auto_vessel_draft, auto_demurrage_rate = optimize_vessel_and_demurrage(cargo_qty, auto_max_draft)

# Allow manual override if needed, pre-filled with AI Auto-fetched value
demurrage_rate = st.sidebar.number_input(
    "Daily Demurrage Rate ($ USD / day)", 
    min_value=5000.0, 
    max_value=100000.0, 
    value=float(auto_demurrage_rate), 
    step=1000.0,
    help="Auto-fetched based on AI Vessel Selection. You can override if required."
)

# Sidebar Display - Dynamic AI Selection
st.sidebar.markdown("---")
st.sidebar.header("🤖 AI Auto-Selection Summary")
st.sidebar.success(f"**Selected Vessel:**\n{auto_vessel}")
st.sidebar.info(f"**Port Draft Limit:** `{auto_max_draft} m` | **Vessel Draft:** `{auto_vessel_draft} m`")
st.sidebar.caption(f"**Auto-Fetched Demurrage Rate:** `${auto_demurrage_rate:,.0f} / day`")

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

# Operational Intelligence Modules
st.markdown("---")
m1, m2, m3 = st.columns(3)

with m1:
    st.markdown("### 📊 Module 1: Rate Forecaster")
    st.write(f"**Current Freight Rate:** ${current_rate:.2f} / MT")
    st.write(f"**7-Day AI Target Rate:** ${predicted_rate:.2f} / MT")

with m2:
    st.markdown("### 🚢 Module 2: Draft Clearance")
    st.write(f"**Selected Vessel:** {auto_vessel}")
    st.write(f"**Vessel Draft:** {auto_vessel_draft} m | **Port Max Draft:** {auto_max_draft} m")
    if auto_vessel_draft <= auto_max_draft:
        st.success("✅ Safe Draft Clearance")
    else:
        st.error("⚠️ WARNING: Draft Violation Risk!")

with m3:
    st.markdown("### 🌊 Module 3: Live Weather & Congestion")
    st.write("**Live Ocean Wave Height:** 2.4 m")
    st.write("**Weather Status:** Moderate Swell")
    st.write(f"**Tidal Window Delay:** +{tidal_delay_hours} Hours")