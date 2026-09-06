import pandas as pd
import requests

class Module3IDEL:
    def __init__(self, congestion_csv="data/congestion.csv", ports_csv="data/ports.csv"):
        self.congestion_csv = congestion_csv
        self.ports_csv = ports_csv
        
        # Extended Coordinates for Major Global & Indian Ports
        self.port_coordinates = {
            "Paradip Port": {"lat": 20.26, "lon": 86.67, "base_depth": 17.5},
            "Visakhapatnam": {"lat": 17.68, "lon": 83.21, "base_depth": 16.5},
            "Dhamra": {"lat": 20.81, "lon": 86.97, "base_depth": 18.0},
            "Haldia": {"lat": 22.02, "lon": 88.06, "base_depth": 12.5},
            "Chennai Port": {"lat": 13.08, "lon": 80.29, "base_depth": 15.5},
            "Kamarajar (Ennore)": {"lat": 13.26, "lon": 80.33, "base_depth": 16.0},
            "Kakinada": {"lat": 16.98, "lon": 82.28, "base_depth": 14.5},
            "Tuticorin (VO Chidambaranar)": {"lat": 8.75, "lon": 78.18, "base_depth": 14.2},
            "Mormugao": {"lat": 15.41, "lon": 73.80, "base_depth": 14.5},
            "Jawaharlal Nehru (JNPT)": {"lat": 18.95, "lon": 72.94, "base_depth": 15.0}
        }

    def fetch_live_marine_telemetry(self, port_name):
        coords = self.port_coordinates.get(port_name, {"lat": 20.26, "lon": 86.67})
        url = f"https://marine-api.open-meteo.com/v1/marine?latitude={coords['lat']}&longitude={coords['lon']}&current=wave_height"
        
        try:
            res = requests.get(url, timeout=3).json()
            wave_height = float(res['current']['wave_height'])
            
            if wave_height >= 3.0:
                weather_status = "Cyclone Alert / Port Halt"
                weather_multiplier = 2.5
            elif wave_height >= 1.8:
                weather_status = "Heavy Swell / Delay Risk"
                weather_multiplier = 1.4
            else:
                weather_status = "Clear / Safe Sea State"
                weather_multiplier = 1.0
                
            return wave_height, weather_status, weather_multiplier
        except Exception:
            return 0.9, "Clear (Cached Stream)", 1.0

    def get_port_telemetry(self, port_name="Paradip Port", vessel_draft=16.5, labor_efficiency=1.0):
        try:
            df = pd.read_csv(self.congestion_csv)
            df.columns = df.columns.str.strip().str.lower()
            time_col = [c for c in df.columns if any(k in c for k in ['wait', 'queue', 'time', 'delay', 'turnaround'])][0]
            raw_queue_val = float(df[time_col].dropna().iloc[0])
            base_queue_hours = raw_queue_val * 24.0 if raw_queue_val < 5.0 else raw_queue_val
        except Exception:
            base_queue_hours = 36.0

        wave_height, weather_status, weather_mult = self.fetch_live_marine_telemetry(port_name)
        port_depth = self.port_coordinates.get(port_name, {}).get("base_depth", 17.5)
        
        depth_margin = port_depth - vessel_draft
        tidal_delay_hrs = 6.0 if depth_margin < 0.5 else 0.0

        final_queue_hours = (base_queue_hours * weather_mult * max(0.8, min(2.0, labor_efficiency))) + tidal_delay_hrs

        return {
            "port_name": port_name,
            "base_queue_hours": round(base_queue_hours, 1),
            "live_wave_height_m": wave_height,
            "weather_status": weather_status,
            "weather_multiplier": weather_mult,
            "tidal_delay_hours": tidal_delay_hrs,
            "anchorage_queue_hours": round(final_queue_hours, 1),
            "waiting_vessels": max(1, int(final_queue_hours / 2.8))
        }