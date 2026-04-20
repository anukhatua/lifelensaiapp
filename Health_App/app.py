from flask import Flask, render_template, request
import joblib
import pandas as pd
import csv
import os

app = Flask(__name__)

# -------- REQUIRED CLASS FOR MODEL --------
class HybridLLM:
    def __init__(self, activity_model, health_model, lifestyle_model, health_columns):
        self.a_model = activity_model
        self.h_model = health_model
        self.l_model = lifestyle_model
        self.health_columns = health_columns

# LOAD MODEL
model = joblib.load("hybrid_llm.pkl")

# -------- PREDICTION FUNCTION --------
def predict_app(steps, calories, heart_rate,
                sleep, activity_level, diet, water, smoking, alcohol):

    health_dict = {}
    health_dict['TotalSteps'] = steps
    health_dict['Calories'] = calories
    health_dict['AvgHeartRate'] = heart_rate

    health_dict['TotalDistance'] = steps * 0.0008
    health_dict['TrackerDistance'] = health_dict['TotalDistance']
    health_dict['LoggedActivitiesDistance'] = 0

    health_dict['VeryActiveDistance'] = health_dict['TotalDistance'] * 0.3
    health_dict['ModeratelyActiveDistance'] = health_dict['TotalDistance'] * 0.2
    health_dict['LightActiveDistance'] = health_dict['TotalDistance'] * 0.5
    health_dict['SedentaryActiveDistance'] = 0

    health_dict['VeryActiveMinutes'] = steps / 200
    health_dict['FairlyActiveMinutes'] = steps / 400
    health_dict['LightlyActiveMinutes'] = steps / 20

    health_dict['SedentaryMinutes'] = max(0, 1440 - (
        health_dict['VeryActiveMinutes'] +
        health_dict['FairlyActiveMinutes'] +
        health_dict['LightlyActiveMinutes']
    ))

    health_data = [health_dict[col] for col in model.health_columns]
    health_input = pd.DataFrame([health_data], columns=model.health_columns)
    health_pred = model.h_model.predict(health_input)[0]

    risk_map = {0: "Low", 1: "Medium", 2: "High"}
    health = risk_map.get(health_pred, "Low")

    score = 0
    if smoking == "Yes": score += 2
    if alcohol == "High": score += 2
    elif alcohol == "Moderate": score += 1
    if activity_level == "Low": score += 2
    elif activity_level == "Moderate": score += 1
    if diet == "Unhealthy": score += 2
    if sleep < 6: score += 2
    elif sleep < 7: score += 1
    if water < 1.5: score += 2
    elif water < 2.5: score += 1

    lifestyle = "High" if score >= 8 else "Medium" if score >= 4 else "Low"

    if lifestyle == "High":
        final = "High Risk"
    elif health in ["High", "Medium"] or lifestyle == "Medium":
        final = "Moderate Risk"
    else:
        final = "Low Risk"

    return health, lifestyle, final


# -------- ROUTES --------

@app.route("/")
def home():
    return render_template("index.html")


@app.route("/analyze")
def analyze():
    return render_template("analyze.html")


@app.route("/loading", methods=["POST"])
def loading():
    return render_template("loading.html", data=request.form)


@app.route("/predict", methods=["POST"])
def predict():

    data = request.form

    age = int(data.get("age", 25))
    gender = data.get("gender", "Male")

    steps = int(data.get("steps", 5000))
    calories = int(data.get("calories", 2000))
    heart_rate = int(data.get("heart_rate", 80))
    sleep = float(data.get("sleep", 7))
    water = float(data.get("water", 2))

    activity = data.get("activity", "Moderate")
    diet = data.get("diet", "Healthy")
    smoking = data.get("smoking", "No")
    alcohol = data.get("alcohol", "No")

    result = predict_app(steps, calories, heart_rate,
                         sleep, activity, diet, water, smoking, alcohol)

    # -------- HEALTH SCORE --------
    score = 0

    if steps >= 7000: score += 20
    elif steps >= 5000: score += 15
    else: score += 8

    ideal_cal = 2500 if gender == "Male" else 2000
    if abs(calories - ideal_cal) <= 300: score += 15
    elif abs(calories - ideal_cal) <= 600: score += 10
    else: score += 5

    if 7 <= sleep <= 9: score += 20
    elif sleep >= 5: score += 12
    else: score += 5

    ideal_water = 3 if gender == "Male" else 2.5
    if water >= ideal_water: score += 15
    elif water >= ideal_water - 1: score += 10
    else: score += 5

    if 60 <= heart_rate <= 100: score += 10
    else: score += 5

    lifestyle_score = 20
    if smoking == "Yes": lifestyle_score -= 5
    if alcohol == "High": lifestyle_score -= 5
    elif alcohol == "Moderate": lifestyle_score -= 2
    if diet == "Healthy": lifestyle_score += 5

    score += lifestyle_score
    final_score = min(score, 100)

    if final_score >= 80:
        status = "Excellent"
    elif final_score >= 60:
        status = "Moderate"
    else:
        status = "Needs Attention"

    # -------- OBSERVATIONS --------
    observations = []

    if steps < 7000:
        observations.append("Your daily movement is below the recommended level.")
    if sleep < 7:
        observations.append("Your sleep pattern may affect recovery and energy levels.")
    if water < ideal_water:
        observations.append("Hydration levels are lower than optimal.")
    if heart_rate > 100:
        observations.append("Elevated heart rate may indicate stress or low fitness.")
    if diet == "Unhealthy":
        observations.append("Diet quality is impacting your overall health.")
    if smoking == "Yes":
        observations.append("Smoking increases long-term health risks.")
    if alcohol in ["Moderate", "High"]:
        observations.append("Alcohol consumption may affect your health.")

    if not observations:
        observations.append("Your overall lifestyle is balanced and healthy.")

    # -------- GUIDANCE / SUGGESTIONS / PLAN --------
    guidance = []
    suggestions = []
    plan = []

    if steps < 5000:
        guidance.append(f"You are currently walking around {steps} steps daily, which is quite low for maintaining good health.")
        plan.append("Start with small goals like 4000-5000 steps and gradually increase to 7000+.")
    elif steps < 7000:
        guidance.append(f"Your daily steps ({steps}) are slightly below the recommended range.")
        plan.append("Try adding short walks or using stairs to reach 7000-10000 steps.")
    else:
        suggestions.append(f"Great job! Your step count ({steps}) is within a healthy range.")

    if sleep < 6:
        guidance.append(f"Your sleep duration is {sleep} hours, which is insufficient for proper recovery.")
        plan.append("Aim for at least 7-8 hours by maintaining a fixed sleep schedule.")
    elif sleep < 7:
        suggestions.append(f"Your sleep ({sleep} hrs) is slightly low.")
        plan.append("Try improving sleep timing and reducing screen time before bed.")
    else:
        suggestions.append("Your sleep pattern is healthy. Maintain consistency.")

    if water < ideal_water - 1:
        guidance.append(f"You are drinking only {water}L of water daily, which is quite low.")
        plan.append(f"Gradually increase water intake to at least {ideal_water}L per day.")
    elif water < ideal_water:
        suggestions.append(f"Your hydration ({water}L) can be improved.")
        plan.append(f"Try reaching {ideal_water}L daily for optimal hydration.")
    else:
        suggestions.append("Your hydration level is good.")

    if heart_rate > 100:
        guidance.append(f"Your heart rate ({heart_rate} BPM) is higher than normal.")
        plan.append("Include relaxation techniques, light cardio, and stress management.")
    elif heart_rate < 60:
        suggestions.append(f"Your heart rate ({heart_rate} BPM) is on the lower side.")
    else:
        suggestions.append("Your heart rate is within a healthy range.")

    if diet == "Unhealthy":
        guidance.append("Your current diet pattern may negatively affect your health.")
        plan.append("Include more whole foods, vegetables, protein, and reduce processed food.")
    else:
        suggestions.append("Your diet looks balanced. Maintain this consistency.")

    if smoking == "Yes":
        guidance.append("Smoking significantly increases long-term health risks.")
        plan.append("Consider reducing gradually and seeking support if needed.")

    if alcohol == "High":
        guidance.append("High alcohol consumption can impact multiple health parameters.")
        plan.append("Try reducing intake frequency and quantity.")
    elif alcohol == "Moderate":
        suggestions.append("Moderate alcohol consumption detected. Keep it controlled.")

    if not guidance and not suggestions:
        guidance.append("You are maintaining an excellent lifestyle.")
        suggestions.append("Focus on consistency and long-term sustainability.")
        plan.append("Maintain your current routine and consider adding light strength training or flexibility exercises.")

    return render_template("result.html",
                           result=result,
                           data=data,
                           score=final_score,
                           status=status,
                           observations=observations,
                           guidance=guidance,
                           suggestions=suggestions,
                           plan=plan)


@app.route("/insights")
def insights():
    return render_template("insights.html")


@app.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        name = request.form.get("name", "")
        email = request.form.get("email", "")
        rating = request.form.get("rating", "")
        message = request.form.get("message", "")

        file_exists = os.path.isfile("feedback.csv")

        with open("feedback.csv", "a", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)

            if not file_exists:
                writer.writerow(["Name", "Email", "Rating", "Message"])

            writer.writerow([name, email, rating, message])

        return render_template("contact.html", success=True)

    return render_template("contact.html")


@app.route("/developer")
def developer():
    return render_template("developer.html")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=7860)