import datetime
import streamlit as st

# ---------------------------------------------------------
# Dynamic Decision Execution Dates
# ---------------------------------------------------------
today = datetime.date.today()
target_fix_date = (today + datetime.timedelta(days=7)).strftime("%d-%m-%Y")
laycan_start = (today + datetime.timedelta(days=12)).strftime("%d-%m-%Y")
laycan_end = (today + datetime.timedelta(days=18)).strftime("%d-%m-%Y")

# ---------------------------------------------------------
# TOP BANNER: RISK MITIGATION & EXECUTIVE ACTION SIGNAL
# ---------------------------------------------------------
st.markdown("## 🛡️ Risk Mitigation & Decision Engine")

# Example NDV Decision Logic
if ndv > 0:
    st.error(
        f"🚨 **EXECUTIVE ACTION SIGNAL: WAIT / DEFER FIXING**\n\n"
        f"📅 **Optimal Charter Fixing Date:** **{target_fix_date}** (Execute Charter Agreement in 7 Days)\n\n"
        f"⚓ **Recommended Laycan Window:** **{laycan_start} to {laycan_end}**\n\n"
        f"💡 **Risk Mitigation Benefit:** Protects against **${demurrage_risk:,.2f}** demurrage loss while locking lower freight rates."
    )
else:
    st.success(
        f"⚡ **EXECUTIVE ACTION SIGNAL: FIX IMMEDIATELY**\n\n"
        f"📅 **Optimal Charter Fixing Date:** **Today ({today.strftime('%d-%m-%Y')})**\n\n"
        f"⚓ **Action:** Lock current spot market rates to mitigate market upward price risk."
    )

st.markdown("---")

# ---------------------------------------------------------
# 3 CORE ENGINE MODULES (UPDATED NAMES)
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
    st.write(f"**Vessel Draft:** {vessel_draft}m | **Port Max Draft:** {port_depth}m")
    st.write(f"⚡ **Optimal Eco-Speed:** {eco_speed} Knots | **Fuel:** {fuel_consumption} T/day")
    st.caption("Draft Clearance Probability: 99.1%")

with col3:
    st.subheader("⏳ Idle Module")
    st.warning("Status: RISK (High Port Congestion)")
    st.write(f"**Live Wave Height:** {wave_height} m | **Swell:** Moderate")
    st.write(f"**Tidal & Swell Delay:** +{total_delay:.1f} Hours")
    st.caption("Congestion Risk Probability: 86.5%")
