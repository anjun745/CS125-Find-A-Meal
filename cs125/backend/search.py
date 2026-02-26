import datetime
from flask import Flask, request, jsonify, Blueprint
from flask_cors import CORS
from .routes.user_info import stored_info
# from . import api_spoonacular as api
from . import recipe_query as rq
import sqlite3
import os
from pathlib import Path
search_bp = Blueprint("search", __name__)
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

stored_query_info = {}  #stores query info...
allergy = None
@search_bp.get("/api/search")
def get_info():  #allows GET requests to /api/search
    return jsonify(stored_query_info)
def _get_calories_per_mealtime():
    cals = stored_info["user_calories_per_day"]

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

    calories_for_meal = int(cals * percentage)

    return meal, calories_for_meal

@search_bp.post("/api/search")
def save_info():
    data = request.get_json()
    stored_info["query"] = data.get("query")
    stored_info["filters"] = data.get("filters")
    #meal_type = "breakfast" #change later to be based on time!!!
    
    #stored_info["meals"] = api.get_meal(stored_info, meal_type)
    global allergy
    try:
        allergy = stored_info["macros"].get("allergies")
    except:
        None

    if allergy:
        allergy = [a.strip().lower() for a in allergy.split(",") if a.strip()]
    else:
        allergy = None

    conn = connect_db()
    create_table(conn)
    ingred = [t.strip().lower() for t in stored_info["query"].split(",") if t.strip()]
    mealtype, calories = _get_calories_per_mealtime()
    macros_check = stored_info["filters"].get("macros")
    calories_check = stored_info["filters"].get("calories")

    carbs = stored_info["macros"].get("carbs")
    mincarbs = None
    maxcarbs = None
    fat = stored_info["macros"].get("fat")
    minfat = None
    maxfat = None
    protein = stored_info["macros"].get("protein")
    minpro = None
    maxpro = None
    if carbs:
        mincarbs = carbs-10
        maxcarbs = carbs+10
    if fat:
        minfat = fat-10
        maxfat = fat+10
    if protein:
        minpro = protein-10
        maxpro = protein+10

    mincal = None
    maxcal = None
    if calories:
        mincal = calories-100
        maxcal = calories+100

    if(calories_check and macros_check):
        print("FILTER: CALORIES & MACROS")
        stored_info["meals"] = rq.query_with_extras(conn, ingred, allergy=allergy,
            min_calories=mincal,
            max_calories=maxcal,
            min_protein=minpro,
            max_protein=maxpro,
            min_carbs=mincarbs,
            max_carbs=maxcarbs,
            min_fat=minfat,
            max_fat=maxfat, meal_type=mealtype)
    elif(macros_check):
        print("FILTER: MACROS")
        stored_info["meals"] = rq.query_with_extras(conn, ingred, allergy=allergy,
            min_calories=None,
            max_calories=None,
            min_protein=minpro,
            max_protein=maxpro,
            min_carbs=mincarbs,
            max_carbs=maxcarbs,
            min_fat=minfat,
            max_fat=maxfat, meal_type=mealtype)
    elif(calories_check):
        print("FILTER: CALORIES")
        stored_info["meals"] = rq.query_with_extras(conn, ingred, allergy=allergy,
            min_calories=mincal,
            max_calories=maxcal, meal_type=mealtype)
    else:
        stored_info["meals"] = rq.query_simple(conn, ingred, allergy, meal_type=mealtype)
        
    return jsonify({
        "status": "search updated",
        "meals": stored_info["meals"]
    })

