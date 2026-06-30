import os
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass
import streamlit as st
import plotly.express as px
import pandas as pd
from data_processing import load_data, clean_data, summarize
from ai_analysis import analyze
from weather import get_weather_for_runs

openweather_key = st.secrets.get("OPENWEATHER_API_KEY", os.getenv("OPENWEATHER_API_KEY", ""))

# ── Page config ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="AI Running Coach",
    page_icon="🏃",
    layout="wide",
)

# ── Custom CSS ─────────────────────────────────────────────────────────────────
st.markdown("""
<style>
    .block-container { padding-top: 2rem; }
    .hero-title {
        font-size: 2.8rem; font-weight: 800;
        letter-spacing: -1px; line-height: 1.1;
    }
    .hero-sub { font-size: 1.1rem; color: #aaa; margin-top: 0.4rem; }
    .section-label {
        font-size: 0.75rem; font-weight: 700;
        letter-spacing: 2px; text-transform: uppercase;
        color: #FF4B4B; margin-bottom: 0.5rem;
    }
    .divider { border: none; border-top: 1px solid #2a2a3e; margin: 1.5rem 0; }
    .feedback-box {
        background: #1A1A2E; border-left: 4px solid #FF4B4B;
        border-radius: 0 8px 8px 0; padding: 1.2rem 1.5rem;
        font-size: 1rem; line-height: 1.8;
    }
    .weather-card {
        background: #1A1A2E; border-radius: 8px;
        padding: 0.8rem 1rem; text-align: center;
        font-size: 0.85rem; color: #ccc;
    }
    .weather-card strong { display: block; font-size: 1.1rem; color: #fff; }
</style>
""", unsafe_allow_html=True)

# ── Sidebar ────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("### 🏃 AI Running Coach")
    st.markdown("Upload your **Garmin Connect Activities CSV** to get a full analysis of your training.")
    st.markdown("---")
    st.markdown("**How to export:**")
    st.markdown("1. Go to [connect.garmin.com](https://connect.garmin.com)")
    st.markdown("2. Activities → All Activities")
    st.markdown("3. Top right → **Export CSV**")
    st.markdown("---")
    if openweather_key:
        st.success("🌤️ Weather API connected")
    else:
        st.warning("⚠️ Set OPENWEATHER_API_KEY in your .env")
    st.markdown("---")
    st.caption("Built for Vibe Coding Final Project · 2026")

# ── Hero ───────────────────────────────────────────────────────────────────────
st.markdown('<div class="hero-title">Your Personal<br>Running Coach 🏃</div>', unsafe_allow_html=True)
st.markdown('<div class="hero-sub">Upload your Garmin data for instant feedback on effort, consistency, pace — and weather.</div>', unsafe_allow_html=True)
st.markdown('<hr class="divider">', unsafe_allow_html=True)

# ── Upload ─────────────────────────────────────────────────────────────────────
uploaded_file = st.file_uploader("Upload your Garmin Activities CSV", type=["csv"], label_visibility="collapsed")

if not uploaded_file:
    st.info("👆 Upload your Garmin Activities CSV to get started.")
    st.stop()

# ── Load & process ─────────────────────────────────────────────────────────────
df = load_data(uploaded_file)
df = clean_data(df)
summary = summarize(df)
paces = summary["pace_floats"]

# ── Metric cards ───────────────────────────────────────────────────────────────
st.markdown('<p class="section-label">Overview</p>', unsafe_allow_html=True)

col1, col2, col3, col4 = st.columns(4)
col1.metric("🏃 Total Runs", summary["total_runs"])
col2.metric("📏 Total Distance", f"{summary['total_distance']} km")
col3.metric("❤️ Avg Heart Rate", f"{summary['avg_heart_rate']:.0f} bpm")

if len(paces) >= 2:
    delta = round(paces[-1] - paces[0], 2)
    col4.metric("⚡ Pace Change", summary["avg_pace"][-1],
                delta=f"{delta:+.2f} min/km", delta_color="inverse")

st.markdown('<hr class="divider">', unsafe_allow_html=True)

# ── Charts ─────────────────────────────────────────────────────────────────────
st.markdown('<p class="section-label">Training Trends</p>', unsafe_allow_html=True)

chart_df = pd.DataFrame({
    "Date":       summary["dates"],
    "Pace":       paces,
    "Distance":   summary["distances"],
    "Heart Rate": summary["heart_rates"],
})

col_a, col_b = st.columns(2)

with col_a:
    fig_pace = px.line(chart_df, x="Date", y="Pace", markers=True,
                       title="Pace over time (min/km)",
                       color_discrete_sequence=["#FF4B4B"])
    fig_pace.update_layout(
        plot_bgcolor="#0E1117", paper_bgcolor="#0E1117", font_color="#FAFAFA",
        xaxis=dict(showgrid=False),
        yaxis=dict(showgrid=True, gridcolor="#2a2a3e", autorange="reversed", title="min/km"),
        margin=dict(l=0, r=0, t=40, b=0), height=260,
    )
    fig_pace.update_traces(line_width=2.5, marker_size=7)
    st.plotly_chart(fig_pace, use_container_width=True)

with col_b:
    fig_hr = px.bar(chart_df, x="Date", y="Heart Rate",
                    title="Heart Rate per run (bpm)",
                    color_discrete_sequence=["#6C63FF"])
    fig_hr.update_layout(
        plot_bgcolor="#0E1117", paper_bgcolor="#0E1117", font_color="#FAFAFA",
        xaxis=dict(showgrid=False),
        yaxis=dict(showgrid=True, gridcolor="#2a2a3e"),
        margin=dict(l=0, r=0, t=40, b=0), height=260,
    )
    st.plotly_chart(fig_hr, use_container_width=True)

st.markdown('<hr class="divider">', unsafe_allow_html=True)

# ── Weather — cached so it never re-fetches on button click ───────────────────
st.markdown('<p class="section-label">🌤️ Weather During Your Runs</p>', unsafe_allow_html=True)

@st.cache_data(show_spinner=False)
def fetch_weather(dates_tuple, api_key):
    return get_weather_for_runs(list(dates_tuple), api_key)

weather_data = {}

if not openweather_key:
    st.info("🌤️ Set OPENWEATHER_API_KEY in your .env to enable weather data.")
else:
    with st.spinner("Fetching weather data from OpenWeatherMap..."):
        try:
            unique_dates = tuple(sorted(set(summary["dates"])))
            weather_data = fetch_weather(unique_dates, openweather_key)

            if weather_data:
                recent_dates = summary["dates"][-6:]
                cols = st.columns(len(recent_dates))
                for i, date in enumerate(recent_dates):
                    w = weather_data.get(date, {})
                    if w:
                        with cols[i]:
                            st.markdown(f"""
                            <div class="weather-card">
                                <strong>{w['condition']}</strong>
                                {date}<br>
                                🌡️ {w['temp']}°C<br>
                                🌧️ {w['precipitation']} mm<br>
                                💨 {w['windspeed']} km/h
                            </div>
                            """, unsafe_allow_html=True)

                weather_rows = []
                for i, (date, pace) in enumerate(zip(summary["dates"], paces)):
                    w = weather_data.get(date)
                    if w:
                        weather_rows.append({
                            "Date": date,
                            "Pace (min/km)": pace,
                            "Temperature (°C)": w["temp"],
                            "Condition": w["condition"],
                            "Distance": summary["distances"][i],
                        })

                if weather_rows:
                    st.markdown("<br>", unsafe_allow_html=True)
                    wdf = pd.DataFrame(weather_rows)
                    fig_scatter = px.scatter(
                        wdf, x="Temperature (°C)", y="Pace (min/km)",
                        color="Condition", size="Distance",
                        hover_data=["Date"],
                        title="Does temperature affect your pace?",
                        color_discrete_sequence=["#FF4B4B","#6C63FF","#00D4AA","#FFB347","#FF6B9D"],
                    )
                    fig_scatter.update_layout(
                        plot_bgcolor="#0E1117", paper_bgcolor="#0E1117", font_color="#FAFAFA",
                        yaxis=dict(autorange="reversed", gridcolor="#2a2a3e"),
                        xaxis=dict(gridcolor="#2a2a3e"),
                        margin=dict(l=0, r=0, t=40, b=0), height=300,
                    )
                    st.plotly_chart(fig_scatter, use_container_width=True)

        except Exception as e:
            st.warning(f"⚠️ Could not fetch weather data: {e}")

st.markdown('<hr class="divider">', unsafe_allow_html=True)

# ── Coach feedback ─────────────────────────────────────────────────────────────
st.markdown('<p class="section-label">Coach Feedback</p>', unsafe_allow_html=True)

if st.button("Analyze my training →", type="primary"):
    with st.spinner("Analyzing your runs..."):
        result = analyze(summary, df)
    lines = result.strip().split("\n")
    formatted = "<br>".join(lines)
    st.markdown(f'<div class="feedback-box">{formatted}</div>', unsafe_allow_html=True)
