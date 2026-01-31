from flask import Flask, request, jsonify, Blueprint
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

userinfo_bp = Blueprint("userinfo", __name__) #used in app.py to run multiple backend files

# in-memory storage (resets when server restarts)
stored_info = {}

def recommended_calories(activity_level, gender, weight, height, age, weight_management):
    weight = weight / 2.20462 #convert lbs to kg
    if gender == 1:  
        bmr = (10 * weight + 6.25 * height - 5 * age + 5) 
    else:  # female
        bmr = (10 * weight + 6.25 * height - 5 * age - 161)

    tdee = bmr * activity_level

    if weight_management == 0: #weight loss 20% deficit
        cal = tdee * 0.8 
    elif weight_management == 1: #maintain
        cal  = tdee
    else: #weight gain 10% surplus
        cal = tdee * 1.1

    return round(cal)

@userinfo_bp.get("/api/info")
def get_info():
    return jsonify(stored_info)

@userinfo_bp.post("/api/info")
def save_info():
    data = request.get_json()
    stored_info["height"] = data.get("height")
    stored_info["weight"] = data.get("weight")
    stored_info["age"] = data.get("age")
    stored_info["gender"] = data.get("gender")
    stored_info["fitness"] = data.get("fitness")
    stored_info["activity"] = data.get("activity")
    stored_info["macros"] = data.get("macros")
    try:
        stored_info["user_calories_per_day"] = recommended_calories(stored_info["activity"], stored_info["gender"], stored_info["weight"], stored_info["height"], 
                                                                    stored_info["age"], stored_info["fitness"])
    except:
        print("Enter required info to get recommended calories.")
    return jsonify({"status": "saved", "data": stored_info})


