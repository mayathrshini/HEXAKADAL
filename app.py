import datetime
import streamlit as st

# ---------------------------------------------------------
# 1. DYNAMIC DATE CALCULATIONS
# ---------------------------------------------------------
today = datetime.date.today()
target_fix_date = (today + datetime.timedelta(days=7)).strftime("%d-%m-%Y")
laycan_start = (today + datetime.timedelta(days=12)).strftime("%d-%m-%Y")
laycan_end = (today + datetime.timedelta(days=18)).strftime("%d-%m-%Y")

# ---------------------------------------------------------
# 2. NDV & COST CALCULATIONS (DEFINING VARIABLES FIRST)
# ---------------------------------------------------------
# Default mock values or pull directly from your module engines
current_rate = 18.50
target_rate = 16.28
cargo_qty = 150000

potential_savings = (current_rate - target_rate) * cargo_qty
demurrage_risk = 32125.0

# Net Decision Value Calculation
ndv = potential_savings - demurrage_risk

# ---------------------------------------------------------
# 3. TOP BANNER: RISK MITIGATION & DECISION ENGINE
# ---------------------------------------------------------
st.markdown("## 🛡️ Risk Mitigation & Decision Engine")

if ndv > 0:
    st.error(
        f"🚨 **EXECUTIVE ACTION SIGNAL: WAIT / DEFER FIXING**\n\n"
        f"📅 **Optimal Charter Fixing Date:** **{target_fix_date}** (Execute fixing in 7 Days)\n\n"
        f"⚓ **Recommended Laycan Window:** **{laycan_start} to {laycan_end}**\n\n"
        f"💡 **Risk Mitigation Benefit:** Saves **${ndv:,.2f}** net after accounting for demurrage risks."
    )
else:
    st.success(
        f"⚡ **EXECUTIVE ACTION SIGNAL: FIX IMMEDIATELY**\n\n"
        f"📅 **Optimal Charter Fixing Date:** **Today ({today.strftime('%d-%m-%Y')})**\n\n"
        f"⚓ **Action:** Lock current spot market rates immediately to avoid price spikes."
    )

st.markdown("---")

# ---------------------------------------------------------
# 4. 3 CORE ENGINE MODULES
# ---------------------------------------------------------
col1, col2, col3 = st.columns(3)

with col1:
    st.subheader("📈 Freight Forecasting Module")
    st.success("Status: CLEAR (Price Drop Forecasted)")
    st.write(f"**Current Freight Rate:** ${current_rate:.2f} / MT")
    st.write(f"**7-Day AI Target Rate:** ${target_rate:.2f} / MT")
    st.caption("Forecast Confidence: 92.4%")

with col2:
    st.subheader("🚢 Vessel Optimization Module")
    st.success("Status: CLEAR (Draft Clearance Passed)")
    st.write("**Vessel Draft:** 16.5m | **Port Max Draft:** 17.5m")
    st.write("⚡ **Optimal Eco-Speed:** 14.2 Knots | **Fuel:** 32.5 T/day")
    st.caption("Draft Clearance Probability: 99.1%")

with col3:
    st.subheader("⏳ Idle Module")
    st.warning("Status: RISK (High Port Congestion)")
    st.write("**Live Wave Height:** 2.4 m | **Swell:** Moderate")
    st.write("**Tidal & Swell Delay:** +25.7 Hours")
    st.caption("Congestion Risk Probability: 86.5%")
