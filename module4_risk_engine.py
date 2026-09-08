import time

class Module4RiskEngine:
    def __init__(self, daily_demurrage_rate=30000.0):
        self.daily_demurrage_rate = daily_demurrage_rate

    def evaluate(self, m1_output, m2_output, m3_output, cargo_volume_mt=150000, live_telemetry=True):
        print("\n" + "="*65)
        print("    HEXAKADAL MODULE 4: RISK MITIGATION & DECISION MATRIX")
        print("="*65)

        if live_telemetry:
            timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
            print(f"[LIVE STREAM ACTIVE] Ingesting Live Telemetry ({timestamp})")

        # ----------------------------------------------------
        # 1. INDIVIDUAL MODULE RISK STATUS ANALYSIS
        # ----------------------------------------------------
        # Module 1 Status (Freight Rate Volatility)
        spot_rate = m1_output.get('current_spot_rate', 0.0)
        forecast_rate = m1_output.get('forecast_spot_rate', 0.0)
        
        if forecast_rate < spot_rate:
            m1_status = "CLEAR (Price Drop Expected)"
            m1_risk = False
        else:
            m1_status = "RISK (Price Spike Expected)"
            m1_risk = True

        # Module 2 Status (Vessel Draft & Port Limit)
        if m2_output.get('is_safe', False):
            m2_status = "CLEAR (Draft Safe)"
            m2_risk = False
        else:
            m2_status = "RISK (Draft Limit Exceeded)"
            m2_risk = True

        # Module 3 Status (Port Queue & Congestion)
        queue_hours = m3_output.get('anchorage_queue_hours', 0.0)
        if queue_hours > 24.0:
            m3_status = "RISK (High Congestion)"
            m3_risk = True
        else:
            m3_status = "CLEAR (Normal Traffic)"
            m3_risk = False

        # ----------------------------------------------------
        # 2. CORE FINANCIAL & NET DECISION VALUE (NDV)
        # ----------------------------------------------------
        rate_delta = spot_rate - forecast_rate
        potential_freight_savings = rate_delta * cargo_volume_mt
        demurrage_cost = (queue_hours / 24.0) * self.daily_demurrage_rate
        net_decision_value = potential_freight_savings - demurrage_cost

        # ----------------------------------------------------
        # 3. EXECUTIVE ACTION SIGNAL GENERATION (XAI)
        # ----------------------------------------------------
        if m2_risk:
            signal = "REROUTE / CANCEL"
            xai_reason = f"Module 2 Alert: Vessel draft ({m2_output.get('vessel_draft')}m) exceeds port berth limit ({m2_output.get('port_max_draft')}m)."
        
        elif net_decision_value > 15000:
            signal = "WAIT (DEFER FIXING)"
            xai_reason = f"Module 1 Clear: Rate dropping to ${forecast_rate}/MT. Net savings (${net_decision_value:,.2f}) exceed demurrage risk."
            
        elif m3_risk or net_decision_value < -10000:
            signal = "FIX IMMEDIATELY"
            xai_reason = f"Module 3 Alert: High port congestion ({queue_hours} hrs) causes heavy demurrage loss (${demurrage_cost:,.2f}). Lock ship now."
            
        else:
            signal = "WATCH MARKET"
            xai_reason = "All metrics within normal tolerance limits."

        return {
            "MODULE_STATUSES": {
                "Module_1_Freight": m1_status,
                "Module_2_Vessel": m2_status,
                "Module_3_IDLE": m3_status
            },
            "FINAL_SIGNAL": signal,
            "NET_DECISION_VALUE_USD": round(net_decision_value, 2),
            "FREIGHT_SAVINGS_USD": round(potential_freight_savings, 2),
            "DEMURRAGE_COST_USD": round(demurrage_cost, 2),
            "XAI_REASON": xai_reason
        }

# ============================================================
# DEMO TEST
# ============================================================
if __name__ == "__main__":
    m1_test = {"current_spot_rate": 18.50, "forecast_spot_rate": 16.28}
    m2_test = {"vessel_draft": 14.2, "port_max_draft": 15.5, "is_safe": True}
    m3_test = {"anchorage_queue_hours": 36.0} # High Congestion Risk

    engine = Module4RiskEngine()
    res = engine.evaluate(m1_test, m2_test, m3_test)

    print("\n--- INDIVIDUAL MODULE STATUS ---")
    for mod, status in res['MODULE_STATUSES'].items():
        print(f"• {mod}: [ {status} ]")

    print(f"\n>>> EXECUTIVE ACTION SIGNAL : [ {res['FINAL_SIGNAL']} ]")
    print(f"-> Net Decision Value (NDV)  : ${res['NET_DECISION_VALUE_USD']:,}")
    print(f"-> Explainable AI Reason    : {res['XAI_REASON']}\n")
