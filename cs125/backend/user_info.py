from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# in-memory storage (resets when server restarts)
stored_info = {}

@app.get("/api/info")
def get_info():
    return jsonify(stored_info)

@app.post("/api/info")
def save_info():
    data = request.get_json()
    stored_info["height"] = data.get("height")
    stored_info["weight"] = data.get("weight")
    stored_info["age"] = data.get("age")
    stored_info["gender"] = data.get("gender")
    return jsonify({"status": "saved", "data": stored_info})

if __name__ == "__main__":
    app.run(debug=True)