from flask import Flask,jsonify
import requests

#alvins api key: 6d081c60d7aa4cd8b2ad2e3c810ef703
API_KEY = "5e1b1107f24d4d1cbc92bb5e681813ab".strip() #use ur own when you can
API_URL = "https://api.spoonacular.com/recipes/complexSearch"
app = Flask(__name__)

def get_info(ingredientList = None,calories = None,protein = None):

    params = {
        "apiKey": API_KEY,
        "query": "chicken",
        "number": 1, #limits results we get to 5
        "addRecipeInformation" : True, #gives us the recipe descriptions
        "addRecipeNutrition" : True,
        "offset": 0,
        "instructionsRequired": True,

    }
        # r is the recipe JSON object
    ingredients_list = []


    # ingredients_list now contains unique ingredient names
    print(ingredients_list)


    response = requests.get(API_URL,params)

    
    print(ingredients_list)
    if response.status_code != 200:#if the request didnt fail
        return jsonify({"error": "API call failed", "status": response.status_code})
    
    data = response.json()
    ingredients_list = []

    # Spoonacular wraps results in "results"
    for r in data.get("results", []):
        for instr in r.get("analyzedInstructions", []):
            for step in instr.get("steps", []):
                for ing in step.get("ingredients", []):
                    name = ing.get("name")
                    if name and name not in ingredients_list:
                        ingredients_list.append(name)

    print(ingredients_list)  # <-- now it will print
    return data  

@app.route("/")   # this handles GET requests to "/"
def home():
    ingredientList = ["chicken","tomato"]
    calories = [0,1000] #range we want our calories in, if we dont care, we return an empty list
    protein = [None,None] #example of when we dont get a response ie the user doesnt care about the protein
    return get_info(ingredientList,calories,protein)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)