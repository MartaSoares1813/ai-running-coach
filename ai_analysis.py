import google.generativeai as genai
import os

def analyze(summary, df):
    try:
        genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
        model = genai.GenerativeModel("gemini-2.0-flash")

        prompt = f"""
You are an expert running coach. Analyze this athlete's training data and give personalized feedback.

- Total runs: {summary['total_runs']}
- Total distance: {summary['total_distance']} km
- Average heart rate: {summary['avg_heart_rate']:.0f} bpm
- Pace history (min/km): {summary['avg_pace']}

Give feedback on effort, consistency, pace progression, and volume. Also, provide tips for improvement.
Keep it concise, specific, and motivating. Use emojis. 
"""
        response = model.generate_content(prompt)
        return response.text

    except Exception:
        # Fallback to rule-based analysis if API is unavailable
        return rule_based_analysis(summary)


def rule_based_analysis(summary):
    feedback = []
    avg_hr     = summary["avg_heart_rate"]
    total_runs = summary["total_runs"]
    paces      = summary["pace_floats"]

    if avg_hr > 170:
        feedback.append("⚠️ High heart rate detected — possible overtraining. Add more easy/recovery runs.")
    elif avg_hr < 150:
        feedback.append("✅ Great aerobic zone training — you're building a solid base.")
    else:
        feedback.append("👍 Balanced effort — heart rate is in a healthy training zone.")

    if total_runs >= 12:
        feedback.append("📅 Excellent consistency — you're running very regularly!")
    elif total_runs >= 6:
        feedback.append("📅 Good training consistency — keep it up!")
    else:
        feedback.append("📉 Try to run more frequently — aim for 3+ runs per week.")

    if len(paces) >= 2:
        improvement = paces[0] - paces[-1]
        if improvement > 0.3:
            feedback.append(f"🚀 Big pace improvement — you're {improvement:.1f} min/km faster than when you started!")
        elif improvement > 0:
            feedback.append("🚀 You're getting faster — great progress!")
        elif improvement < -0.2:
            feedback.append("⚖️ Pace has slowed slightly — check rest and recovery.")
        else:
            feedback.append("⚖️ Pace is stable — keep pushing for that next breakthrough!")

    total_km = summary["total_distance"]
    if total_km > 100:
        feedback.append(f"🏆 Over {total_km:.0f} km logged — serious mileage!")
    elif total_km > 50:
        feedback.append(f"💪 {total_km:.0f} km logged — solid training block.")
    else:
        feedback.append(f"📈 {total_km:.0f} km so far — keep building your weekly volume gradually.")

    feedback.append("\n_(AI quota reached — showing rule-based analysis)_")
    return "\n".join(feedback)