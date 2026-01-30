from flask import Flask, request, jsonify, Blueprint
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

userinfo_bp = Blueprint("userinfo", __name__) #used in app.py to run multiple backend files

# in-memory storage (resets when server restarts)
stored_info = {}

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
    return jsonify({"status": "saved", "data": stored_info})
