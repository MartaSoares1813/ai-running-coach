import requests
from datetime import datetime

# Porto coordinates (fixed — all your runs are in Porto)
PORTO_LAT = 41.1579
PORTO_LON = -8.6291

def get_weather_for_runs(dates: list, api_key: str) -> dict:
    """
    Fetch historical weather for a list of date strings (YYYY-MM-DD).
    Uses OpenWeatherMap History API (One Call 3.0 timemachine).
    Returns: { "2026-06-23": { temp, precipitation, windspeed, condition } }
    """
    result = {}

    for date_str in dates:
        try:
            # Convert date to unix timestamp (noon that day)
            dt = datetime.strptime(date_str, "%Y-%m-%d").replace(hour=12)
            timestamp = int(dt.timestamp())

            url = (
                f"https://api.openweathermap.org/data/3.0/onecall/timemachine"
                f"?lat={PORTO_LAT}&lon={PORTO_LON}"
                f"&dt={timestamp}"
                f"&units=metric"
                f"&appid={api_key}"
            )

            response = requests.get(url, timeout=10)
            response.raise_for_status()
            data = response.json()

            # data["data"] is a list of hourly entries for that day
            hours = data.get("data", [])
            if not hours:
                continue

            temps   = [h["temp"] for h in hours if "temp" in h]
            wind    = [h["wind_speed"] for h in hours if "wind_speed" in h]
            rain    = sum(h.get("rain", {}).get("1h", 0) for h in hours)
            weather = hours[len(hours)//2].get("weather", [{}])[0]
            desc    = weather.get("description", "").capitalize()
            icon_id = weather.get("id", 800)

            avg_temp  = round(sum(temps) / len(temps), 1) if temps else None
            avg_wind  = round(sum(wind)  / len(wind)  * 3.6, 1) if wind else None  # m/s → km/h
            total_rain = round(rain, 1)

            # Pick emoji from weather code
            if icon_id < 300:
                condition = f"⛈️ {desc}"
            elif icon_id < 400:
                condition = f"🌧️ {desc}"
            elif icon_id < 600:
                condition = f"🌧️ {desc}"
            elif icon_id < 700:
                condition = f"❄️ {desc}"
            elif icon_id < 800:
                condition = f"🌫️ {desc}"
            elif icon_id == 800:
                condition = f"☀️ {desc}"
            else:
                condition = f"⛅ {desc}"

            result[date_str] = {
                "temp":          avg_temp,
                "precipitation": total_rain,
                "windspeed":     avg_wind,
                "condition":     condition,
            }

        except Exception as e:
            # Skip this date silently if API call fails
            print(f"Weather fetch failed for {date_str}: {e}")
            continue

    return result
