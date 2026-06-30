# 🏃 AI Running Coach

A personal running analytics app built with Streamlit that analyses your Garmin training data and gives you AI-powered coaching feedback — including real weather conditions for every run.

Built as a final project for the **Vibe Coding** course.

---

## 🚀 Features

- 📊 **Training overview** — total runs, distance, average heart rate, and pace trend
- 📈 **Interactive charts** — pace over time and heart rate per run (Plotly)
- 🌤️ **Weather integration** — fetches real historical weather for each run date via OpenWeatherMap API (cached to avoid repeated calls)
- 🌡️ **Temperature vs Pace analysis** — scatter chart showing how weather conditions affect your performance
- 🤖 **AI Coach feedback** — powered by Google's Gemini API, with automatic fallback to rule-based analysis if the AI quota is reached

---

## 🗂️ Project Structure

```
ai-running-coach/
├── app.py                  # Streamlit frontend
├── data_processing.py      # CSV loading, cleaning, and summarising
├── ai_analysis.py          # AI + rule-based coaching feedback logic
├── weather.py              # OpenWeatherMap API integration
├── requirements.txt        # Python dependencies
├── .env                    # API keys (not committed)
├── .gitignore
└── .streamlit/
    └── config.toml         # Dark theme config
```

---

## 📦 Installation

**1. Clone the repository**
```bash
git clone https://github.com/YOUR_USERNAME/ai-running-coach.git
cd ai-running-coach
```

**2. Create and activate a virtual environment**
```bash
python -m venv venv
venv\Scripts\activate        # Windows
source venv/bin/activate     # Mac/Linux
```

**3. Install dependencies**
```bash
pip install -r requirements.txt
```

**4. Set up your API keys**

Create a `.env` file in the project root:
```
OPENWEATHER_API_KEY=your_openweather_key_here
GEMINI_API_KEY=your_gemini_key_here
```

- Get a free OpenWeatherMap key at [openweathermap.org](https://openweathermap.org/api) — requires subscribing to **One Call API 3.0** (free up to 1,000 calls/day)
- Get a free Gemini key at [aistudio.google.com](https://aistudio.google.com)

---

## ▶️ Running the App

```bash
streamlit run app.py
```

---

## 📥 How to Export Your Garmin Data

1. Go to [connect.garmin.com](https://connect.garmin.com)
2. Navigate to **Activities → All Activities**
3. Click **Export CSV** in the top right
4. Upload the downloaded file in the app

---

# 🧪 Try it with sample data
A sample Garmin export is included at `sample_data/sample_activities.csv` — upload this file in the app to test it without needing your own Garmin account.

## 🛠️ Tech Stack

| Tool | Purpose |
|---|---|
| Python | Core language |
| Streamlit | Frontend / UI |
| Pandas | Data processing |
| Plotly | Interactive charts |
| Google Gemini API | AI-generated coaching feedback |
| OpenWeatherMap API | Historical weather data |
| python-dotenv | Environment variable management |

---

## 👩‍💻 Author

Built by **Marta Soares** · Vibe Coding Final Project · 2026
