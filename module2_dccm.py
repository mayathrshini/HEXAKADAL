import pandas as pd

class Module2DCCM:
    def __init__(self, vessel_csv="data/vessels.csv", port_csv="data/ports.csv"):
        self.vessel_csv = vessel_csv
        self.port_csv = port_csv

    def check_draft_compatibility(self, vessel_id=None, target_port="Paradip"):
        try:
            # Read Vessels CSV
            df_vessels = pd.read_csv(self.vessel_csv)
            df_vessels.columns = df_vessels.columns.str.strip().str.lower()
            
            # Find draft column
            draft_col = [c for c in df_vessels.columns if 'draft' in c][0]
            vessel_draft = float(df_vessels[draft_col].dropna().iloc[0])
        except Exception:
            vessel_draft = 16.5  # Standard Capesize draft (m)

        try:
            # Read Ports CSV
            df_ports = pd.read_csv(self.port_csv)
            df_ports.columns = df_ports.columns.str.strip().str.lower()
            
            # Find port depth/draft column
            port_draft_col = [c for c in df_ports.columns if 'draft' in c or 'depth' in c][0]
            port_max_draft = float(df_ports[port_draft_col].dropna().iloc[0])
        except Exception:
            port_max_draft = 17.5  # Standard Paradip berth depth (m)

        # Draft Margin Math
        draft_margin = port_max_draft - vessel_draft
        is_safe = draft_margin >= 0.5

        return {
            "vessel_draft": round(vessel_draft, 2),
            "port_max_draft": round(port_max_draft, 2),
            "draft_margin": round(draft_margin, 2),
            "is_safe": is_safe
        }

if __name__ == "__main__":
    # Test Module 2 independently
    m2 = Module2DCCM()
    print("Module 2 Test Output:", m2.check_draft_compatibility())