import time

class Module4RiskEngine:
    def __init__(self, daily_demurrage_rate=30000.0):
        """
        Module 4: Risk Mitigation & Decision Support Engine
        Aggregates outputs from:
        - Module 1: XGBoost Freight Forecaster
        - Module 2: Heuristic Vessel/Draft Solver
        - Module 3: IDLE / Port Congestion Model
        """
        self.daily_demurrage_rate = daily_demurrage_rate

    def evaluate(self, m1_output, m2_output, m3_output, cargo_volume_mt=150000, live_telemetry=True):
        print("\n" + "="*65)
        print("    HEXAKADAL MODULE 4: RISK MITIGATION & DECISION MATRIX")
        print("="*65)

        # Live telemetry status check
        if live_telemetry:
            timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
            print(f"[LIVE STREAM ACTIVE] Processing Telemetry & Feeds ({timestamp})")
        else:
            print("[BATCH MODE] Processing Historical Dataset Inputs")

        # ----------------------------------------------------
        # 1. INDIVIDUAL MODULE STATUS & RISK EVALUATION
        # ----------------------------------------------------
        spot_rate = m1_output.get('current_spot_rate', 0.0)
        forecast_rate = m1_output.get('forecast_spot_rate', 0.0)
        queue_hours = m3_output.get('anchorage_queue_hours', 0.0)

        # Module 1 Status (Freight Trend)
        if forecast_rate < spot_rate:
            m1_status = "CLEAR (Price Drop Forecasted)"
            m1_risk = False
        else:
            m1_status = "RISK (Price Spike Forecasted)"
            m1_risk = True

        # Module 2 Status (Vessel & Draft Clearance)
        if m2_output.get('is_safe', False):
            m2_status = "CLEAR (Draft Clearance Passed)"
            m2_risk = False
        else:
            m2_status = "RISK (Draft Limit Exceeded)"
            m2_risk = True

        # Module 3 Status (Port Congestion)
        if queue_hours > 24.0:
            m3_status = "RISK (High Port Congestion)"
            m3_risk = True
        else:
            m3_status = "CLEAR (Normal Port Queue)"
            m3_risk = False

        # ----------------------------------------------------
        # 2. CORE FINANCIAL MATH (NET DECISION VALUE)
        # ----------------------------------------------------
        # Potential Freight Savings from XGBoost Prediction
        rate_delta = spot_rate - forecast_rate
        potential_freight_savings = rate_delta * cargo_volume_mt

        # Demurrage Cost Risk Calculation
        demurrage_cost = (queue_hours / 24.0) * self.daily_demurrage_rate

        # Net Decision Value (NDV)
        net_decision_value = potential_freight_savings - demurrage_cost

        # ----------------------------------------------------
        # 3. EXPLAINABLE AI (XAI) ACTION SIGNAL GENERATION
        # ----------------------------------------------------
        if m2_risk:
            signal = "REROUTE / CANCEL"
            xai_reason = (f"Module 2 Hard Constraint Violation: Vessel draft ({m2_output.get('vessel_draft')}m) "
                          f"exceeds port max draft limit ({m2_output.get('port_max_draft')}m). Grounding risk.")

        elif net_decision_value > 15000:
            signal = "WAIT (DEFER FIXING)"
            xai_reason = (f"Module 1 Clear: Rate predicted to drop from ${spot_rate}/MT to ${forecast_rate}/MT. "
                          f"Expected Net Savings after demurrage (${demurrage_cost:,.2f}): ${net_decision_value:,.2f}.")

        elif m3_risk or net_decision_value < -10000:
            signal = "FIX IMMEDIATELY"
            xai_reason = (f"Module 3 Alert: High port congestion ({queue_hours} hrs) causes heavy demurrage risk "
                          f"(${demurrage_cost:,.2f}). Lock vessel now to prevent loss.")

        else:
            signal = "WATCH MARKET"
            xai_reason = f"Stable market conditions. Net Decision Value (${net_decision_value:,.2f}) within normal threshold."

        return {
            "MODULE_STATUSES": {
                "Module_1_Freight": m1_status,
                "Module_2_Draft": m2_status,
                "Module_3_IDLE": m3_status
            },
            "FINAL_SIGNAL": signal,
            "NET_DECISION_VALUE_USD": round(net_decision_value, 2),
            "FREIGHT_SAVINGS_USD": round(potential_freight_savings, 2),
            "DEMURRAGE_COST_USD": round(demurrage_cost, 2),
            "XAI_REASON": xai_reason
        }

# ============================================================
# DEMO EXECUTION
# ============================================================
if __name__ == "__main__":
    # Simulated outputs from Modules 1, 2, and 3
    m1_xgboost = {"current_spot_rate": 18.50, "forecast_spot_rate": 16.28}
    m2_heuristic = {"vessel_draft": 14.2, "port_max_draft": 15.5, "is_safe": True}
    m3_idle = {"anchorage_queue_hours": 36.0}  # High congestion

    engine = Module4RiskEngine(daily_demurrage_rate=30000.0)
    result = engine.evaluate(m1_xgboost, m2_heuristic, m3_idle)

    print("\n--- INDIVIDUAL MODULE STATUS ---")
    for mod, status in result['MODULE_STATUSES'].items():
        print(f"• {mod}: [ {status} ]")

    print(f"\n>>> EXECUTIVE ACTION SIGNAL : [ {result['FINAL_SIGNAL']} ]")
    print(f"-> Net Decision Value (NDV)  : ${result['NET_DECISION_VALUE_USD']:,}")
    print(f"-> Freight Savings          : ${result['FREIGHT_SAVINGS_USD']:,}")
    print(f"-> Demurrage Risk Cost      : ${result['DEMURRAGE_COST_USD']:,}")
    print(f"-> Explainable AI Reason    : {result['XAI_REASON']}\n")
