from flask import Flask, request, jsonify, Blueprint
from flask_cors import CORS
from .routes.user_info import stored_info
# from . import api_spoonacular as api
from . import recipe_query as rq
import sqlite3
import os
from pathlib import Path

def create_table(conn):
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS recipes (
        id INTEGER PRIMARY KEY,
        title TEXT,
        summary TEXT,
        instructions TEXT,
        ingredients TEXT,
        calories INT,
        protein INT,
        fat INT,
        fiber INT,
        image_url TEXT,
        servings INT,
        ready_in_minutes INT,
        source_url TEXT,
        diets TEXT,
        cuisines TEXT,
        very_healthy BOOL,
        like_count INT,
        spoonacular_score REAL,
        meal_type TEXT
                
    )
    """)
    conn.commit()


BASE_DIR = Path(__file__).resolve().parent

def get_db_path():
    return BASE_DIR / "recipes.db"

def connect_db():
    print("PATH: ", get_db_path())
    conn = sqlite3.connect(get_db_path())
    conn.row_factory = sqlite3.Row
    return conn

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
    #meal_type = "breakfast" #change later to be based on time!!!
    
    #stored_info["meals"] = api.get_meal(stored_info, meal_type)
    
    conn = connect_db()
    create_table(conn)
    ingred = [t.strip().lower() for t in stored_info["query"].split(",") if t.strip()]
    print("query:", ingred)
    stored_info["meals"] = rq.query_simple(conn, ingred)
    return jsonify({
        "status": "search updated",
        "meals": stored_info["meals"]
    })

