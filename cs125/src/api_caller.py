from flask import Flask,jsonify
import requests
import json

#alvins api key: 6d081c60d7aa4cd8b2ad2e3c810ef703
API_KEY = "".strip() #use ur own when you can
API_URL = "https://api.spoonacular.com/recipes/complexSearch"
app = Flask(__name__)

def get_info():
    headers = {"Authorization": f"Bearer {API_KEY}"}

    response = requests.get(API_URL,headers)

    if response == 200:#if the request didnt fail
        return jsonify(response.json())
    else:
        return jsonify({"error": "API call failed", "status": response.status_code})

@app.route("/")   # this handles GET requests to "/"
def home():
    return get_info()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80)