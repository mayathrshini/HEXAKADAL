import streamlit as st
import pandas as pd
from module1_forecaster import Module1FreightForecaster
from module2_dccm import Module2DCCM
from module3_idel import Module3IDEL
from module4_risk_engine import Module4RiskEngine

st.set_page_config(page_title="HEXAKADAL - Ocean Suite", page_icon="⚓", layout="wide")

# 🌊 HIGH-CONTRAST OCEAN CSS
st.markdown("""
    <style>
    .stApp {
        background-color: #0b192c;
        color: #f8fafc;
    }
    section[data-testid="stSidebar"] {
        background-color: #1e3e62;
    }
    /* Metric Label Text Styling */
    div[data-testid="stMetricLabel"] > label {
        color: #94a3b8 !important;
        font-size: 0.95rem !important;
        font-weight: 600 !important;
    }
    div[data-testid="stMetricValue"] {
        color: #38bdf8 !important;
        font-weight: 700 !important;
    }
    /* Text Color Enhancements */
    h1, h2, h3, h4, label, p, span {
        color: #f8fafc !important;
    }
    </style>
""", unsafe_allow_html=True)

# 🎯 MAIN HEADER WITH SPECIFIC PROJECT DESCRIPTION
st.title("⚓ HEXAKADAL")
st.subheader("AI-Based Ocean Freight Engine for Bulk Cargo Procurement to India's East Coast")
st.caption("Commercial Decision Support System for Chartering Managers & Port Operations (Values in USD)")

st.divider()

# Clean Commercial Bulk Carriers
ship_list = [
    "MV ORE BRASIL (400k DWT Valemax)",
    "MV BERGE BULKER (180k DWT Capesize)",
    "MV PACIFIC OAK (180k DWT Capesize)",
    "MV BAY PRIDE (75k DWT Panamax)",
    "MV OCEAN STAR (58k DWT Supramax)"
]

global_origins = [
    "Hay Point (Australia)", "Dampier (Australia)", "Port Hedland (Australia)", 
    "Richards Bay (South Africa)", "Saldanha Bay (South Africa)", "Tubarao (Brazil)", 
    "Newcastle (Australia)", "Port Samarinda (Indonesia)"
]

indian_dests = [
    "Paradip Port", "Visakhapatnam", "Dhamra", "Haldia", "Chennai Port", 
    "Kamarajar (Ennore)", "Kakinada", "Tuticorin (VO Chidambaranar)", "Mormugao", "Jawaharlal Nehru (JNPT)"
]

# ----------------------------------------------------
# 🕹️ MANAGER VOYAGE INPUTS
# ----------------------------------------------------
st.sidebar.header("📋 Voyage & Cargo Parameters")

selected_vessel = st.sidebar.selectbox("Select Vessel", ship_list)
cargo_vol = st.sidebar.number_input("Cargo Quantity (Metric Tons)", value=150000, step=10000)
daily_demurrage = st.sidebar.number_input("Daily Demurrage Rate ($ USD / day)", value=30000.0, step=1000.0)

col_p1, col_p2 = st.sidebar.columns(2)
origin_port = col_p1.selectbox("Origin Port", global_origins)
dest_port = col_p2.selectbox("Destination Port (India)", indian_dests)

st.sidebar.divider()
st.sidebar.header("🚢 Vessel & Port Operations")
vessel_draft_input = st.sidebar.slider("Vessel Draft Depth (Meters)", 12.0, 18.5, 16.5, step=0.1)
labor_eff = st.sidebar.slider("Port Operations Efficiency", 0.8, 1.5, 1.0, step=0.1)

# ----------------------------------------------------
# ⚙️ EXECUTION ENGINE
# ----------------------------------------------------
m1 = Module1FreightForecaster()
m2 = Module2DCCM()
m3 = Module3IDEL()
m4 = Module4RiskEngine(daily_demurrage_rate=daily_demurrage)

m1_res = m1.predict_15d_rate()
m2_res = m2.check_draft_compatibility(target_port=dest_port)
m2_res['vessel_draft'] = vessel_draft_input
m2_res['is_safe'] = (m2_res['port_max_draft'] - vessel_draft_input) >= 0.5

m3_res = m3.get_port_telemetry(port_name=dest_port, vessel_draft=vessel_draft_input, labor_efficiency=labor_eff)
final_eval = m4.evaluate(m1_res, m2_res, m3_res, cargo_volume_mt=cargo_vol)

# ----------------------------------------------------
# 📊 EXECUTIVE DASHBOARD UI
# ----------------------------------------------------
signal = final_eval['FINAL_SIGNAL']
if "WAIT" in signal:
    st.warning(f"### 🔥 EXECUTIVE ACTION SIGNAL: **{signal}**")
elif "ENTER" in signal:
    st.success(f"### 🔥 EXECUTIVE ACTION SIGNAL: **{signal}**")
else:
    st.error(f"### 🔥 EXECUTIVE ACTION SIGNAL: **{signal}**")

st.info(f"💡 **Explainable AI (XAI) Rationale:** {final_eval['XAI_REASON']}")

# Financial Metrics in USD
m1_col, m2_col, m3_col, m4_col = st.columns(4)
m1_col.metric("Net Decision Value (NDV in USD)", f"${final_eval['NET_DECISION_VALUE_USD']:,}")
m2_col.metric("Potential Freight Savings (USD)", f"${final_eval['FREIGHT_SAVINGS_USD']:,}")
m3_col.metric("Demurrage Loss Risk (USD)", f"${final_eval['DEMURRAGE_COST_USD']:,}")
m4_col.metric("Total Congestion Queue", f"{m3_res['anchorage_queue_hours']} Hours")

st.divider()

# Subsystem Telemetry Cards
st.subheader("📌 Multi-Stream Operational Telemetry")
c1, c2, c3 = st.columns(3)

with c1:
    st.markdown("#### 📈 Module 1: Freight Market")
    st.write(f"**Vessel Assigned:** {selected_vessel}")
    st.write(f"**Route:** {origin_port} ➔ {dest_port}")
    st.write(f"**Current Spot Rate:** ${m1_res['current_spot_rate']} USD/MT")
    st.write(f"**15-Day Forward Rate:** ${m1_res['forecast_spot_rate']} USD/MT")

with c2:
    st.markdown("#### ⚓ Module 2: Berth & Draft Safety")
    st.write(f"**Vessel Draft:** {vessel_draft_input} m")
    st.write(f"**{dest_port} Depth Limit:** {m2_res['port_max_draft']} m")
    if m2_res['is_safe']:
        st.success("✅ Safe Draft Clearance")
    else:
        st.error("❌ CRITICAL: Draft Limit Violation!")

with c3:
    st.markdown("#### 🌊 Module 3: Live Weather & Congestion")
    st.write(f"**Live Ocean Wave Height:** {m3_res['live_wave_height_m']} m")
    st.write(f"**Weather Status:** {m3_res['weather_status']}")
    st.write(f"**Tidal Window Delay:** +{m3_res['tidal_delay_hours']} Hours")
    st.write(f"**Waiting Vessels:** ~{m3_res['waiting_vessels']} Ships")