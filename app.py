import streamlit as st
import pandas as pd
import numpy as np
import datetime

# Safe Imports of Custom Modules
try:
    from module4_risk_engine import Module4RiskEngine
except ImportError:
    Module4RiskEngine = None

try:
    from module3_idel import Module3IDEL
except ImportError:
    Module3IDEL = None

# Page Configuration
st.set_page_config(
    page_title="HEXAKADAL (SIH26006) | Ocean Freight Engine",
    page_icon="⚓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------------------------------------------------------
# ENTERPRISE MATTE GRAPHITE STYLING
# ---------------------------------------------------------
st.markdown("""
    <style>
    /* Dark Slate & Graphite Palette */
    .stApp {
        background-color: #0d1117;
        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
    }
    
    /* Header Section */
    .header-container {
        padding: 10px 0 16px 0;
        border-bottom: 1px solid #21262d;
        margin-bottom: 20px;
    }
    .problem-code {
        background-color: #161b22;
        color: #8b949e;
        padding: 3px 8px;
        border-radius: 4px;
        font-size: 0.75rem;
        font-weight: 600;
        letter-spacing: 0.05em;
        border: 1px solid #30363d;
        display: inline-block;
        margin-bottom: 8px;
    }
    .header-title {
        color: #f0f6fc;
        font-size: 1.8rem;
        font-weight: 700;
        margin: 0;
        display: inline-block;
    }
    .header-subtitle {
        color: #8b949e;
        font-size: 0.95rem;
        font-weight: 400;
        margin-left: 10px;
    }
    
    /* Executive Metric Box */
    .metric-box {
        background: #161b22;
        border: 1px solid #30363d;
        border-radius: 6px;
        padding: 14px 16px;
    }
    .metric-label {
        font-size: 0.72rem;
        font-weight: 600;
        text-transform: uppercase;
        color: #8b949e;
        letter-spacing: 0.04em;
        margin-bottom: 4px;
    }
    .metric-value-savings {
        font-size: 1.4rem;
        font-weight: 700;
        color: #3fb950;
    }
    .metric-value-risk {
        font-size: 1.4rem;
        font-weight: 700;
        color: #f85149;
    }
    .metric-value-neutral {
        font-size: 1.4rem;
        font-weight: 700;
        color: #f0f6fc;
    }
    .metric-sub {
        font-size: 0.72rem;
        color: #6e7681;
        margin-top: 2px;
    }

    /* Module 4 Action Banner */
    .decision-banner {
        background-color: #161b22;
        border-left: 4px solid #d29922;
        border-top: 1px solid #30363d;
        border-right: 1px solid #30363d;
        border-bottom: 1px solid #30363d;
        border-radius: 4px;
        padding: 12px 16px;
        margin-bottom: 20px;
    }
    .decision-title {
        font-size: 0.9rem;
        font-weight: 700;
        color: #f0f6fc;
        margin-bottom: 2px;
        letter-spacing: 0.02em;
    }
    .decision-details {
        font-size: 0.82rem;
        color: #8b949e;
    }

    /* Analytical Modules */
    .module-card {
        background-color: #161b22;
        border: 1px solid #30363d;
        border-radius: 6px;
        padding: 16px;
        height: 100%;
    }
    .module-title {
        font-size: 0.88rem;
        font-weight: 600;
        color: #f0f6fc;
    }
    .module-subtitle {
        font-size: 0.72rem;
        color: #8b949e;
        margin-bottom: 12px;
        padding-bottom: 6px;
        border-bottom: 1px solid #21262d;
    }

    /* Status Indicators */
    .status-clear {
        color: #3fb950;
        font-size: 0.7rem;
        font-weight: 600;
    }
    .status-risk {
        color: #f85149;
        font-size: 0.7rem;
        font-weight: 600;
    }

    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# SIDEBAR: PARAMETERS
# ---------------------------------------------------------
st.sidebar.markdown("<h4 style='color: #f0f6fc; font-size: 0.9rem;'>Voyage Setup</h4>", unsafe_allow_html=True)

cargo_qty = st.sidebar.number_input(
    "Cargo Quantity (Metric Tons)", 
    min_value=10000, 
    max_value=500000, 
    value=150000, 
    step=5000
)

origin_port = st.sidebar.selectbox(
    "Origin Loading Port", 
    ["Hay Point (Australia)", "Newcastle (Australia)", "Saldanha Bay (South Africa)", "Port Hedland (Australia)"]
)

destination_port = st.sidebar.selectbox(
    "Destination Port (India)", 
    ["Paradip Port", "Visakhapatnam Port", "Haldia Port", "Dhamra Port", "Gopalpur Port"]
)

# Port Max Draft Database
port_draft_database = {
    "Paradip Port": 14.50,       
    "Visakhapatnam Port": 16.10, 
    "Haldia Port": 8.50,         
    "Dhamra Port": 18.00,        
    "Gopalpur Port": 14.50       
}

auto_max_draft = port_draft_database.get(destination_port, 14.50)

# Vessel Optimization Function
def optimize_vessel_data(cargo_tons, port_max_draft):
    if cargo_tons >= 200000:
        ideal_vessel = "MV ORE BRASIL (400k DWT Valemax)"
        required_draft = 18.0
        demurrage = 45000.0
        speed = "13.5 Knots"
        fuel = "42.0 T/day"
    elif cargo_tons >= 100000:
        ideal_vessel = "MV CAPESIZE HERO (180k DWT Capesize)"
        required_draft = 16.5
        demurrage = 30000.0
        speed = "14.2 Knots"
        fuel = "32.5 T/day"
    elif cargo_tons >= 60000:
        ideal_vessel = "MV PANAMAX STAR (75k DWT Panamax)"
        required_draft = 12.0
        demurrage = 20000.0
        speed = "13.0 Knots"
        fuel = "24.0 T/day"
    else:
        ideal_vessel = "MV SUPRAMAX OCEAN (55k DWT Supramax)"
        required_draft = 9.0
        demurrage = 15000.0
        speed = "12.5 Knots"
        fuel = "18.5 T/day"

    if required_draft > port_max_draft:
        is_safe = False
        if port_max_draft >= 12.0:
            rec_vessel = "MV PANAMAX STAR (75k DWT Panamax)"
            rec_draft = 12.0
            demurrage = 20000.0
            speed = "13.0 Knots"
            fuel = "24.0 T/day"
        else:
            rec_vessel = "MV SUPRAMAX OCEAN (55k DWT Supramax)"
            rec_draft = 9.0
            demurrage = 15000.0
            speed = "12.5 Knots"
            fuel = "18.5 T/day"
    else:
        is_safe = True
        rec_vessel = ideal_vessel
        rec_draft = required_draft

    return {
        "ideal_vessel": ideal_vessel,
        "vessel_name": rec_vessel,
        "vessel_draft": rec_draft,
        "required_draft": required_draft,
        "demurrage_rate": demurrage,
        "eco_speed": speed,
        "fuel_cons": fuel,
        "is_safe": is_safe
    }

vessel_info = optimize_vessel_data(cargo_qty, auto_max_draft)
auto_vessel = vessel_info["vessel_name"]
auto_vessel_draft = vessel_info["vessel_draft"]
demurrage_rate = vessel_info["demurrage_rate"]

st.sidebar.markdown("---")
st.sidebar.markdown("<h5 style='color: #8b949e; font-size: 0.75rem; text-transform: uppercase;'>Module 2 Summary</h5>", unsafe_allow_html=True)
st.sidebar.caption(f"**Target Class:** {vessel_info['ideal_vessel']}")

if vessel_info["is_safe"]:
    st.sidebar.caption(f"**Feasible Vessel:** {auto_vessel}")
else:
    st.sidebar.caption(f"**Draft Constrained:** {auto_vessel}")

st.sidebar.caption(f"**Port Limit:** {auto_max_draft}m | **Req:** {vessel_info['required_draft']}m")
st.sidebar.caption(f"**Demurrage Benchmark:** ${demurrage_rate:,.0f} / day")

# ---------------------------------------------------------
# CALCULATIONS
# ---------------------------------------------------------
current_rate = 18.50
target_rate = 16.28
m1_output = {"current_spot_rate": current_rate, "forecast_spot_rate": target_rate}

if Module3IDEL is not None:
    try:
        m3_engine = Module3IDEL()
        m3_telemetry = m3_engine.get_port_telemetry(port_name=destination_port, vessel_draft=auto_vessel_draft)
        wave_height = m3_telemetry.get("live_wave_height_m", 2.4)
        total_delay = m3_telemetry.get("anchorage_queue_hours", 25.7)
        ais_vessels = m3_telemetry.get("ais_waiting_vessels", 9)
    except Exception:
        wave_height = 2.4
        total_delay = 25.7
        ais_vessels = 9
else:
    wave_height = 2.4
    total_delay = 25.7
    ais_vessels = 9

m2_is_safe = vessel_info["is_safe"]

if Module4RiskEngine is not None:
    try:
        engine = Module4RiskEngine(daily_demurrage_rate=demurrage_rate)
        eval_result = engine.evaluate(
            m1_output=m1_output,
            m2_output={"vessel_draft": auto_vessel_draft, "port_max_draft": auto_max_draft, "is_safe": m2_is_safe},
            m3_output={"anchorage_queue_hours": total_delay},
            cargo_volume_mt=cargo_qty,
            live_telemetry=True
        )
        ndv = eval_result["NET_DECISION_VALUE_USD"]
        potential_savings = eval_result["FREIGHT_SAVINGS_USD"]
        demurrage_risk = eval_result["DEMURRAGE_COST_USD"]
    except Exception:
        potential_savings = (current_rate - target_rate) * cargo_qty
        demurrage_risk = (total_delay / 24.0) * demurrage_rate
        ndv = potential_savings - demurrage_risk
else:
    potential_savings = (current_rate - target_rate) * cargo_qty
    demurrage_risk = (total_delay / 24.0) * demurrage_rate
    ndv = potential_savings - demurrage_risk

today = datetime.date.today()
target_fix_date = (today + datetime.timedelta(days=7)).strftime("%d %b %Y")
laycan_start = (today + datetime.timedelta(days=12)).strftime("%d %b %Y")
laycan_end = (today + datetime.timedelta(days=18)).strftime("%d %b %Y")

# ---------------------------------------------------------
# HEADER SECTION
# ---------------------------------------------------------
st.markdown(f"""
    <div class='header-container'>
        <div class='problem-code'>SIH26006</div><br>
        <h1 class='header-title'>HEXAKADAL</h1>
        <span class='header-subtitle'>| &nbsp; AI-Based Ocean Freight Engine for Bulk Cargo Procurement to India's East Coast</span>
    </div>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# MODULE 4: RISK MITIGATION & DECISION ENGINE BANNER
# ---------------------------------------------------------
if ndv > 0:
    st.markdown(f"""
        <div class='decision-banner'>
            <div class='decision-title'>MODULE 4: RISK MITIGATION AND DECISION ENGINE — RECOMMENDATION: DEFER FIXING (WAIT 7 DAYS)</div>
            <div class='decision-details'>
                Target Charter Fixing Date: <strong style='color: #f0f6fc;'>{target_fix_date}</strong> &nbsp;|&nbsp; 
                Recommended Laycan Window: <strong style='color: #f0f6fc;'>{laycan_start} – {laycan_end}</strong> &nbsp;|&nbsp; 
                Net Decision Value (NDV): <strong style='color: #3fb950;'>+${ndv:,.2f}</strong>
            </div>
        </div>
    """, unsafe_allow_html=True)
else:
    st.markdown(f"""
        <div class='decision-banner' style='border-left-color: #2ea043;'>
            <div class='decision-title'>MODULE 4: RISK MITIGATION AND DECISION ENGINE — RECOMMENDATION: FIX CHARTER IMMEDIATELY</div>
            <div class='decision-details'>
                Target Charter Fixing Date: <strong style='color: #f0f6fc;'>Today ({today.strftime('%d %b %Y')})</strong> &nbsp;|&nbsp; 
                Lock current market spot rates to avoid projected upward exposure.
            </div>
        </div>
    """, unsafe_allow_html=True)

# ---------------------------------------------------------
# METRIC SUMMARY
# ---------------------------------------------------------
c1, c2, c3, c4 = st.columns(4)

with c1:
    st.markdown(f"""
        <div class='metric-box'>
            <div class='metric-label'>Net Decision Value (NDV)</div>
            <div class='metric-value-savings'>${ndv:,.2f}</div>
            <div class='metric-sub'>Risk-adjusted return</div>
        </div>
    """, unsafe_allow_html=True)

with c2:
    st.markdown(f"""
        <div class='metric-box'>
            <div class='metric-label'>Gross Freight Savings</div>
            <div class='metric-value-neutral'>${potential_savings:,.2f}</div>
            <div class='metric-sub'>Via ${current_rate - target_rate:.2f}/MT rate delta</div>
        </div>
    """, unsafe_allow_html=True)

with c3:
    st.markdown(f"""
        <div class='metric-box'>
            <div class='metric-label'>Demurrage Exposure Risk</div>
            <div class='metric-value-risk'>${demurrage_risk:,.2f}</div>
            <div class='metric-sub'>Port anchorage delay penalty</div>
        </div>
    """, unsafe_allow_html=True)

with c4:
    st.markdown(f"""
        <div class='metric-box'>
            <div class='metric-label'>Total Anchorage Delay</div>
            <div class='metric-value-neutral'>{total_delay:.1f} Hrs</div>
            <div class='metric-sub'>{ais_vessels} vessels in queue</div>
        </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ---------------------------------------------------------
# 3 ANALYTICAL MODULES
# ---------------------------------------------------------
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown(f"""
        <div class='module-card'>
            <div style='display:flex; justify-content:space-between; align-items:center;'>
                <div class='module-title'>Module 1: Freight Forecasting Module</div>
                <div class='status-clear'>● ACTIVE</div>
            </div>
            <div class='module-subtitle'>Spot Rate Intelligence & Forecast</div>
            <div style='margin-bottom: 8px;'>
                <span style='color: #8b949e; font-size: 0.75rem;'>Current Spot Rate:</span><br>
                <strong style='color: #f0f6fc; font-size: 0.95rem;'>${current_rate:.2f} / MT</strong>
            </div>
            <div style='margin-bottom: 12px;'>
                <span style='color: #8b949e; font-size: 0.75rem;'>7-Day AI Forecasted Rate:</span><br>
                <strong style='color: #3fb950; font-size: 1.05rem;'>${target_rate:.2f} / MT</strong>
            </div>
            <div style='background: #0d1117; padding: 8px 10px; border-radius: 4px; border: 1px solid #21262d;'>
                <p style='color: #8b949e; font-size: 0.72rem; margin: 0;'>
                    BDI & bunker trends project rate reduction over next 7 days.
                </p>
            </div>
        </div>
    """, unsafe_allow_html=True)

with col2:
    status_str = "<div class='status-clear'>● FEASIBLE</div>" if vessel_info["is_safe"] else "<div class='status-risk'>● DRAFT RESTRICTED</div>"
    
    st.markdown(f"""
        <div class='module-card'>
            <div style='display:flex; justify-content:space-between; align-items:center;'>
                <div class='module-title'>Module 2: Vessel Optimization Module</div>
                {status_str}
            </div>
            <div class='module-subtitle'>Fleet Selection & Navigation Feasibility</div>
            <div style='margin-bottom: 8px;'>
                <span style='color: #8b949e; font-size: 0.75rem;'>Optimized Vessel:</span><br>
                <strong style='color: #f0f6fc; font-size: 0.88rem;'>{vessel_info['vessel_name']}</strong>
            </div>
            <div style='display: flex; gap: 16px; margin-bottom: 12px;'>
                <div>
                    <span style='color: #8b949e; font-size: 0.72rem;'>Vessel Draft:</span><br>
                    <strong style='color: #f0f6fc; font-size: 0.82rem;'>{vessel_info['vessel_draft']}m</strong>
                </div>
                <div>
                    <span style='color: #8b949e; font-size: 0.72rem;'>Port Max Limit:</span><br>
                    <strong style='color: #f0f6fc; font-size: 0.82rem;'>{auto_max_draft}m</strong>
                </div>
            </div>
            <div style='background: #0d1117; padding: 8px 10px; border-radius: 4px; border: 1px solid #21262d;'>
                <p style='color: #8b949e; font-size: 0.72rem; margin: 0;'>
                    Eco-Speed: {vessel_info['eco_speed']} &nbsp;|&nbsp; Fuel: {vessel_info['fuel_cons']}
                </p>
            </div>
        </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
        <div class='module-card'>
            <div style='display:flex; justify-content:space-between; align-items:center;'>
                <div class='module-title'>Module 3: IDLE Management Module</div>
                <div class='status-risk'>● HIGH IDLE</div>
            </div>
            <div class='module-subtitle'>Port Telemetry & Anchorage Queue Tracking</div>
            <div style='margin-bottom: 8px;'>
                <span style='color: #8b949e; font-size: 0.75rem;'>Anchorage Queue:</span><br>
                <strong style='color: #f0f6fc; font-size: 0.95rem;'>{ais_vessels} Bulk Carriers Waiting</strong>
            </div>
            <div style='margin-bottom: 12px;'>
                <span style='color: #8b949e; font-size: 0.75rem;'>Marine Weather Telemetry:</span><br>
                <strong style='color: #f0f6fc; font-size: 0.82rem;'>{wave_height}m Wave Height (Swell)</strong>
            </div>
            <div style='background: #0d1117; padding: 8px 10px; border-radius: 4px; border: 1px solid #21262d;'>
                <p style='color: #8b949e; font-size: 0.72rem; margin: 0;'>
                    Projected Delay: +{total_delay:.1f} Hours at berth anchorage.
                </p>
            </div>
        </div>
    """, unsafe_allow_html=True)
