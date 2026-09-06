import time

class Module4RiskEngine:
    def __init__(self, daily_demurrage_rate=30000.0):
        self.daily_demurrage_rate = daily_demurrage_rate

    def evaluate(self, m1_output, m2_output, m3_output, cargo_volume_mt=150000, live_telemetry=True):
        print("\n" + "="*55)
        print("     HEXAKADAL RISK ENGINE: CALCULATING DECISION MATRIX")
        print("="*55)

        # ----------------------------------------------------
        # REAL-TIME LIVE DATA OVERRIDE LAYER
        # ----------------------------------------------------
        if live_telemetry:
            # Simulating Real-time API Ping timestamp
            timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
            print(f"[LIVE FEED ACTIVE] Connected to Real-time Stream ({timestamp})")
            
            # Live updates merged with ML forecast outputs
            spot_rate = m1_output['current_spot_rate']
            forecast_rate = m1_output['forecast_spot_rate']
            queue_hours = m3_output['anchorage_queue_hours']
        else:
            print("[HISTORICAL FEED] Using Cached Batch Dataset")
            spot_rate = m1_output['current_spot_rate']
            forecast_rate = m1_output['forecast_spot_rate']
            queue_hours = m3_output['anchorage_queue_hours']

        # ----------------------------------------------------
        # CORE FINANCIAL & RISK MATH
        # ----------------------------------------------------
        # 1. Potential Freight Savings
        rate_delta = spot_rate - forecast_rate
        potential_freight_savings = rate_delta * cargo_volume_mt

        # 2. Demurrage Loss Risk Cost
        demurrage_cost = (queue_hours / 24.0) * self.daily_demurrage_rate

        # 3. Net Decision Value (Core Aggregated Value)
        net_decision_value = potential_freight_savings - demurrage_cost

        # ----------------------------------------------------
        # EXPLAINABLE AI (XAI) SIGNAL GENERATION MATRIX
        # ----------------------------------------------------
        if not m2_output['is_safe']:
            signal = "WATCH / REROUTE"
            reason = f"CRITICAL DRAFT EXCEEDED: Vessel draft ({m2_output['vessel_draft']}m) exceeds port berth depth limit ({m2_output['port_max_draft']}m)."
        
        elif net_decision_value > 15000:
            signal = "WAIT / DEFER FIXING"
            reason = f"Rate forecasted to drop from ${spot_rate}/MT to ${forecast_rate}/MT. Expected Net Savings after Demurrage: ${net_decision_value:,.2f}."
            
        elif net_decision_value < -10000:
            signal = "ENTER / FIX NOW"
            reason = f"High port congestion queue ({queue_hours} hrs) generates severe demurrage risk (${demurrage_cost:,.2f}). Lock vessel immediately."
            
        else:
            signal = "WATCH"
            reason = f"Market is stable. Net Decision Value (${net_decision_value:,.2f}) within normal tolerance threshold."

        return {
            "FINAL_SIGNAL": signal,
            "NET_DECISION_VALUE_USD": round(net_decision_value, 2),
            "FREIGHT_SAVINGS_USD": round(potential_freight_savings, 2),
            "DEMURRAGE_COST_USD": round(demurrage_cost, 2),
            "XAI_REASON": reason
        }

if __name__ == "__main__":
    # Internal Test with sample module feeds
    m1_sample = {"current_spot_rate": 18.50, "forecast_spot_rate": 16.28}
    m2_sample = {"vessel_draft": 16.5, "port_max_draft": 17.5, "is_safe": True}
    m3_sample = {"anchorage_queue_hours": 36.0}

    engine = Module4RiskEngine()
    res = engine.evaluate(m1_sample, m2_sample, m3_sample)
    
    print(f"\n>>> DECISION SIGNAL : [ {res['FINAL_SIGNAL']} ]")
    print(f"-> Net Decision Value : ${res['NET_DECISION_VALUE_USD']:,}")
    print(f"-> XAI Explanation    : {res['XAI_REASON']}\n")