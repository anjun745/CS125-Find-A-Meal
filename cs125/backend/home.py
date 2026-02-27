import datetime
from flask import Flask, request, jsonify, Blueprint
from flask_cors import CORS
from .routes.user_info import stored_info
from . import recipe_query as rq
import sqlite3
from pathlib import Path

home_bp = Blueprint("home", __name__)


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

def _get_calories_per_mealtime():
    now = datetime.datetime.now().hour

    if 5 <= now < 11:
        meal = "breakfast"
        percentage = 0.25
    elif 11 <= now < 16:
        meal = "lunch"
        percentage = 0.35
    else:
        meal = "dinner"
        percentage = 0.40

    return meal

APP_STATE = {}

stored_query_info = {}  #stores query info...
allergy = None
@home_bp.get("/api/home")
def get_info():  #allows GET requests to /api/homr
    conn = connect_db()
    create_table(conn)

    mealtype = _get_calories_per_mealtime()

    allergy = None
    try:
        allergy = stored_info["macros"].get("allergies")
    except Exception:
        allergy = None

    if allergy:
        allergy = [a.strip().lower() for a in allergy.split(",") if a.strip()]
    else:
        allergy = None

    carbs = stored_info.get("macros", {}).get("carbs")
    fat = stored_info.get("macros", {}).get("fat")
    protein = stored_info.get("macros", {}).get("protein")

    mincarbs = carbs - 10 if carbs else None
    maxcarbs = carbs + 10 if carbs else None
    minfat   = fat - 10 if fat else None
    maxfat   = fat + 10 if fat else None
    minpro   = protein - 10 if protein else None
    maxpro   = protein + 10 if protein else None

    meals = rq.recommendations(
        conn,
        allergy=allergy,
        meal_type=mealtype,
        limit=20
    )
    return jsonify({
        "status": "home recommendations",
        "meal_type": mealtype,
        "meals": meals
    })