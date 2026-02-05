from flask import Flask,jsonify
import requests

#alvins api key: 6d081c60d7aa4cd8b2ad2e3c810ef703
API_KEY = "6d081c60d7aa4cd8b2ad2e3c810ef703".strip() #use ur own when you can
API_URL = "https://api.spoonacular.com/recipes/complexSearch"
app = Flask(__name__)

def get_info(ingredientList = None,calories = None,protein = None):

    params = {
        "apiKey": API_KEY,
        "number": 5, #limits results we get to 5
        "addRecipeInformation" : True, #gives us the recipe descriptions
        "addRecipeNutrition" : True

    }
    if ingredientList: #if they dont care about ingredients dont add it to the search query
        params["includeIngredients"] = ",".join(ingredientList), 
    
    minmax_map = {
        "calories" : ("minCalories","maxCalories"),
        "protein" : ("minProtein","maxProtein")
    }

    for value, (min,max) in [           #BASICALLY, we are checking if the user entered if they care about calories or entered a range of calories/protein they want
                                        #if they DID NOT then we don't add it to the URL when using our API
        (calories, minmax_map["calories"]),
        (protein, minmax_map["protein"])]:
        if value: 
            if value[0]:
                params[min] = value[0]
            if value[1]:
                params[max] = [max]
        

    response = requests.get(API_URL,params)

    if response.status_code == 200:#if the request didnt fail
        return jsonify(response.json())
    else:
        return jsonify({"error": "API call failed", "status": response.status_code})

@app.route("/")   # this handles GET requests to "/"
def home():
    ingredientList = ["chicken","tomato"]
    calories = [0,1000] #range we want our calories in, if we dont care, we return an empty list
    protein = [None,None] #example of when we dont get a response ie the user doesnt care about the protein
    return get_info(ingredientList,calories,protein)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)