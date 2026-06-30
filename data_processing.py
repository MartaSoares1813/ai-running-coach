
import pandas as pd

def load_data(file):
    df = pd.read_csv(file)
    return df

def clean_data(df):
    # Keep only running activities
    df = df[df["Tipo de atividade"] == "Corrida"].copy()

    # Parse date
    df["Data"] = pd.to_datetime(df["Data"])
    df["date_str"] = df["Data"].dt.strftime("%Y-%m-%d")
    df["hour"] = df["Data"].dt.hour

    # Distance & HR to numeric
    df["Distância"] = pd.to_numeric(df["Distância"], errors="coerce")
    df["RC médio"]  = pd.to_numeric(df["RC médio"],  errors="coerce")

    # Sort oldest → newest
    df = df.sort_values("Data").reset_index(drop=True)

    return df

def summarize(df):
    def pace_to_float(pace_str):
        try:
            m, s = str(pace_str).strip().split(":")
            return float(m) + float(s) / 60
        except:
            return None

    pace_floats = df["Ritmo médio"].apply(pace_to_float).dropna().tolist()

    summary = {
        "total_runs":      len(df),
        "total_distance":  round(df["Distância"].sum(), 1),
        "avg_heart_rate":  round(df["RC médio"].mean(), 0),
        "avg_pace":        df["Ritmo médio"].tolist(),
        "pace_floats":     pace_floats,
        "dates":           df["date_str"].tolist(),
        "distances":       df["Distância"].tolist(),
        "heart_rates":     df["RC médio"].tolist(),
    }
    return summary