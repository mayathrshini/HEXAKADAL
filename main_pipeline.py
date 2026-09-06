from module1_forecaster import Module1FreightForecaster
from module2_dccm import Module2DCCM
from module3_idel import Module3IDEL
from module4_risk_engine import Module4RiskEngine

def run_hexakadal_system():
    print("\n" + "="*70)
    print("      HEXAKADAL: END-TO-END MARITIME RISK MITIGATION SYSTEM")
    print("="*70)

    # 1. Initialize All Feeder Modules & Risk Engine
    m1 = Module1FreightForecaster()
    m2 = Module2DCCM()
    m3 = Module3IDEL()
    m4 = Module4RiskEngine(daily_demurrage_rate=30000.0)

    print("\n[STEP 1] Fetching Multi-Stream Datasets & Real-Time Inferences...")
    
    # 2. Execute Sub-system Inferences
    m1_res = m1.predict_15d_rate()
    m2_res = m2.check_draft_compatibility()
    m3_res = m3.get_port_telemetry(port_name="Paradip Port")

    print(f"  └─► [M1 Freight] Spot: ${m1_res['current_spot_rate']}/MT | 15d Forecast: ${m1_res['forecast_spot_rate']}/MT")
    print(f"  └─► [M2 DCCM] Vessel Draft: {m2_res['vessel_draft']}m | Port Depth: {m2_res['port_max_draft']}m | Margin Safe: {m2_res['is_safe']}")
    print(f"  └─► [M3 IDEL] Port Anchorage Queue: {m3_res['anchorage_queue_hours']} Hours at {m3_res['port_name']}")

    # 3. Core Brain Risk Evaluation
    print("\n[STEP 2] Aggregating Feeder Data into Module 4 Decision Matrix...")
    final_eval = m4.evaluate(m1_res, m2_res, m3_res, cargo_volume_mt=150000, live_telemetry=True)

    # 4. Final Output Dashboard Presentation
    print("\n" + "─"*70)
    print(f" 🔥 EXECUTIVE ACTION SIGNAL : [ {final_eval['FINAL_SIGNAL']} ]")
    print("─"*70)
    print(f"  💵 Net Decision Value (NDV)   : ${final_eval['NET_DECISION_VALUE_USD']:,}")
    print(f"  📈 Expected Freight Savings   : ${final_eval['FREIGHT_SAVINGS_USD']:,}")
    print(f"  ⚠️  Demurrage Risk Penalty    : ${final_eval['DEMURRAGE_COST_USD']:,}")
    print(f"  💡 XAI Reason / Explanation   : {final_eval['XAI_REASON']}")
    print("="*70 + "\n")

if __name__ == "__main__":
    run_hexakadal_system()