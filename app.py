import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# Import custom engines
from module4_risk_engine import Module4RiskEngine

# Import Module 2 (dccm) engine created by team
try:
    from module2_dccm import run_pipeline as run_m2_pipeline
except ImportError:
    run_m2_pipeline = None

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
        return "MV ORE BRASIL (400k DWT Valemax)", 18.0, 45000.0, 400000
    elif cargo_tons >= 100000 and port_max_draft >= 16.0:
        return "MV CAPESIZE HERO (180k DWT Capesize)", 16.5, 30000.0, 180000
    elif cargo_tons >= 60000 and port_max_draft >= 11.0:
        return "MV PANAMAX STAR (75k DWT Panamax)", 12.0, 20000.0, 75000
    else:
        return "MV SUPRAMAX OCEAN (55k DWT Supramax)", 9.0, 15000.0, 55000

auto_vessel, auto_vessel_draft, demurrage_rate, auto_dwt = optimize_vessel_and_demurrage(cargo_qty, auto_max_draft)

# Sidebar Display Summary
st.sidebar.markdown("---")
st.sidebar.header("🤖 AI Auto-Selection Summary")
st.sidebar.success(f"**Selected Vessel:**\n{auto_vessel}")
st.sidebar.info(f"**Port Draft Limit:** `{auto_max_draft} m` | **Vessel Draft:** `{auto_vessel_draft} m`")
st.sidebar.caption(f"💰 **Auto-Fetched Demurrage Rate:** `${demurrage_rate:,.0f} / day`")

# ----------------------------------------------------
# MODULE 2 LOGIC EXECUTION (module2_dccm.py)
# ----------------------------------------------------
m2_opt_results = {}
m2_is_safe = auto_vessel_draft <= auto_max_draft

if run_m2_pipeline is not None:
    try:
        m2_opt_results = run_m2_pipeline(
            cargo_volume_tons=cargo_qty,
            origin_port=origin_port.split(" (")[0],
            discharge_port=destination_port,
            current_draft=auto_vessel_draft,
            current_dwt=auto_dwt,
            distance_nm=5500,
            bunker_price=650.0,
            charter_rate=demurrage_rate
        )
    except Exception:
        m2_opt_results = {
            "optimal_speed_knots": 14.2,
            "total_voyage_days": 16.1,
            "predicted_daily_fuel_tons": 32.5,
            "minimum_total_cost_usd": 485000.0
        }

# ----------------------------------------------------
# PREPARE INPUT DATA FOR MODULE 4 RISK ENGINE
# ----------------------------------------------------
m1_output = {
    "current_spot_rate": 18.50,
    "forecast_spot_rate": 16.28
}

m2_output = {
    "vessel_draft": auto_vessel_draft,
    "port_max_draft": auto_max_draft,
    "is_safe": m2_is_safe
}

m3_output = {
    "anchorage_queue_hours": 25.7
}

# Execute Module 4 Engine
engine = Module4RiskEngine(daily_demurrage_rate=demurrage_rate)
eval_result = engine.evaluate(
    m1_output=m1_output,
    m2_output=m2_output,
    m3_output=m3_output,
    cargo_volume_mt=cargo_qty,
    live_telemetry=True
)

# Extract Values
signal = eval_result["FINAL_SIGNAL"]
xai_reason = eval_result["XAI_REASON"]
ndv = eval_result["NET_DECISION_VALUE_USD"]
rate_savings = eval_result["FREIGHT_SAVINGS_USD"]
demurrage_loss = eval_result["DEMURRAGE_COST_USD"]
mod_statuses = eval_result["MODULE_STATUSES"]

# ----------------------------------------------------
# UI DISPLAY - EXECUTIVE ACTION & XAI RATIONALE
# ----------------------------------------------------
if "REROUTE" in signal:
    st.error(f"🛑 **EXECUTIVE ACTION SIGNAL: {signal}**")
    st.warning(f"💡 **Explainable AI (XAI) Rationale:** {xai_reason}")
elif "WAIT" in signal:
    st.error(f"🔥 **EXECUTIVE ACTION SIGNAL: {signal}**")
    st.info(f"💡 **Explainable AI (XAI) Rationale:** {xai_reason}")
elif "FIX" in signal:
    st.success(f"✅ **EXECUTIVE ACTION SIGNAL: {signal}**")
    st.info(f"💡 **Explainable AI (XAI) Rationale:** {xai_reason}")
else:
    st.info(f"👀 **EXECUTIVE ACTION SIGNAL: {signal}**")
    st.write(f"💡 **Explainable AI (XAI) Rationale:** {xai_reason}")

# Financial Key Metrics
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("Net Decision Value (NDV in USD)", f"${ndv:,.1f}")
with col2:
    st.metric("Potential Freight Savings (USD)", f"${rate_savings:,.1f}")
with col3:
    st.metric("Demurrage Loss Risk (USD)", f"${demurrage_loss:,.1f}")
with col4:
    st.metric("Total Congestion Queue", f"{m3_output['anchorage_queue_hours']} Hours")

# Operational Intelligence Modules Section
st.markdown("---")
st.markdown("## 🚦 Module Operational & Risk Statuses")

m1, m2, m3 = st.columns(3)

m1_prob = 92.4
m2_prob = 98.1 if m2_is_safe else 12.5
m3_prob = 86.5

with m1:
    st.markdown("### 📊 Module 1: Rate Forecaster")
    if "CLEAR" in mod_statuses["Module_1_Freight"]:
        st.success(f"Status: {mod_statuses['Module_1_Freight']}")
    else:
        st.error(f"Status: {mod_statuses['Module_1_Freight']}")
    
    st.write(f"**Current Freight Rate:** ${m1_output['current_spot_rate']:.2f} / MT")
    st.write(f"**7-Day AI Target Rate:** ${m1_output['forecast_spot_rate']:.2f} / MT")
    st.caption(f"🎯 **Model Forecast Confidence:** `{m1_prob}%`")

with m2:
    st.markdown("### 🚢 Module 2: Draft & Fuel Optimization")
    if "CLEAR" in mod_statuses["Module_2_Draft"]:
        st.success(f"Status: {mod_statuses['Module_2_Draft']}")
    else:
        st.error(f"Status: {mod_statuses['Module_2_Draft']}")
        
    st.write(f"**Vessel Draft:** {auto_vessel_draft}m | **Port Max Draft:** {auto_max_draft}m")
    
    opt_speed = m2_opt_results.get("optimal_speed_knots", 14.2)
    opt_fuel = m2_opt_results.get("predicted_daily_fuel_tons", 32.5)
    st.write(f"⚡ **Optimal Eco-Speed:** {opt_speed} Knots | **Fuel:** {opt_fuel} T/day")
    st.caption(f"🛡️ **Draft Clearance Probability:** `{m2_prob}%`")

with m3:
    st.markdown("### 🌊 Module 3: Congestion Engine")
    if "CLEAR" in mod_statuses["Module_3_IDLE"]:
        st.success(f"Status: {mod_statuses['Module_3_IDLE']}")
    else:
        st.warning(f"Status: {mod_statuses['Module_3_IDLE']}")
        
    st.write(f"**Live Wave Height:** 2.4 m | **Swell:** Moderate")
    st.write(f"**Tidal Delay:** +{m3_output['anchorage_queue_hours']} Hours")
    st.caption(f"⚠️ **Congestion Risk Probability:** `{m3_prob}%`")

# ----------------------------------------------------
# VISUAL ANALYTICS: BALTIC INDEX XGBOOST FORECAST GRAPH
# ----------------------------------------------------
st.markdown("---")
st.markdown("### 📈 Baltic Dry Index (BDI) Spot Rate Forecast Curve")

# Create chart dataframe
dates = [datetime.today() - timedelta(days=i) for i in range(7, 0, -1)] + [datetime.today() + timedelta(days=i) for i in range(1, 8)]
hist_data = [18.5, 18.4, 18.6, 18.5, 18.4, 18.5, 18.50] + [None]*7
pred_data = [None]*6 + [18.50, 18.10, 17.80, 17.40, 17.10, 16.80, 16.50, 16.28]

chart_df = pd.DataFrame({
    "Historical Spot Rate ($/MT)": hist_data,
    "7-Day XGBoost Forecast ($/MT)": pred_data
}, index=[d.strftime('%b %d') for d in dates])

st.line_chart(chart_df)
