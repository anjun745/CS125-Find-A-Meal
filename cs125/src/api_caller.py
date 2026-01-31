from flask import Flask,jsonify
import requests

#alvins api key: 6d081c60d7aa4cd8b2ad2e3c810ef703
API_KEY = "6d081c60d7aa4cd8b2ad2e3c810ef703".strip() #use ur own when you can
API_URL = "https://api.spoonacular.com/recipes/complexSearch"
app = Flask(__name__)

def get_info(ingredientList = None):
    if ingredientList is None:
        ingredientList = [] #i just dont like having default mutable arguments
        


    params = {
        "apiKey": API_KEY,
        "includeIngredients": ",".join(ingredientList), #list of ingredients to be included
        "number": 5 #limits results we get to 5
    }

    response = requests.get(API_URL,params)

    if response.status_code == 200:#if the request didnt fail
        return jsonify(response.json())
    else:
        return jsonify({"error": "API call failed", "status": response.status_code})

@app.route("/")   # this handles GET requests to "/"
def home():
    ingredientList = ["chicken","tomato"]
    return get_info(ingredientList)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)