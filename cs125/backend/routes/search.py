from flask import Flask, request, jsonify, Blueprint
from flask_cors import CORS
from routes.user_info import stored_info
app = Flask(__name__)
CORS(app)

search_bp = Blueprint("search", __name__)
stored_query_info = {}  #stores query info...

@search_bp.get("/api/search")
def get_info():  #allows GET requests to /api/search
    stored_info.update(stored_query_info)  #combines user info with search query info (shows up on user-info page)
    return jsonify(stored_query_info)

@search_bp.post("/api/search")
def save_info():
    data = request.get_json()
    # Process search data here -> api search and filters etc...
    stored_query_info.update(data) #stores the search query data into our in-memory storage
    return jsonify({"status": "search data received", "data": stored_query_info})