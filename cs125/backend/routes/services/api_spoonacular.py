import requests

MEAL_WEIGHTS = {
    "breakfast": 0.25,
    "lunch": 0.375,
    "dinner": 0.375
}

leah_api = "41b38bcafc974c06937752cda574f500"
API_KEY = ""#leah_api
API_URL = "https://api.spoonacular.com/recipes/complexSearch"

def meal_calorie_range(daily_calories: int, meal: str, tolerance=0.1):
    '''returns a tuple which describes a range of how many calories we need to return based on what the current
    meal time is'''
    target = daily_calories * MEAL_WEIGHTS[meal]
    return (
        int(target * (1 - tolerance)),
        int(target * (1 + tolerance))
    )

def get_recipes_for_meal(meal, user_calories_per_day,ingredients=None,query=None,macros=None):
    min_cal, max_cal = meal_calorie_range(
        user_calories_per_day,
        meal
    )

    params = {
        "apiKey": API_KEY,
        "number": 5,
        "type": meal,
        "minCalories": min_cal,
        "maxCalories": max_cal,
        "addRecipeInformation": True
    }

    if ingredients:
        params["includeIngredients"] = ",".join(ingredients)

    if query:
        params["query"] = query

    if macros:
        if macros.get("protein"):
            params["minProtein"] = macros["protein"]
        if macros.get("fiber"):
            params["minFiber"] = macros["fiber"]
        if macros.get("fat"):
            params["maxFat"] = macros["fat"]

    response = requests.get(API_URL, params=params)
    return response.json()

def get_meal(user_state, meal_type):
    '''@param meal_type: "breakfast", "lunch", or "dinner"'''
    calories = user_state["user_calories_per_day"]
    macros = user_state.get("macros")
    query = user_state.get("query")
    ingredients = user_state.get("ingredients")

    return {
        "meal-result": get_recipes_for_meal(
            meal_type,
            calories,
            ingredients,
            query,
            macros
        )
    }