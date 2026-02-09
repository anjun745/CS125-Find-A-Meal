from flask import Flask, request, jsonify, Blueprint
from flask_cors import CORS
from .user_info import stored_info
from .services import api_spoonacular as api

APP_STATE = {}

search_bp = Blueprint("search", __name__)
stored_query_info = {}  #stores query info...

@search_bp.get("/api/search")
def get_info():  #allows GET requests to /api/search
    return jsonify(stored_query_info)

@search_bp.post("/api/search")
def save_info():
    data = request.get_json()
    stored_info["query"] = data.get("query")
    stored_info["filters"] = data.get("filters")
    meal_type = "breakfast" #change later to be based on time!!! 
    stored_info["meals"] = api.get_meal(stored_info, meal_type)

    return jsonify({
        "status": "search updated",
        "meals": stored_info["meals"]
    })