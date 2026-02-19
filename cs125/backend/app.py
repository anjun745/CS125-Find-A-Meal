from flask import Flask
from flask_cors import CORS
from .routes import userinfo_bp
from .routes import search_bp

app = Flask(__name__)
CORS(app)

app.register_blueprint(userinfo_bp)
app.register_blueprint(search_bp)

if __name__ == "__main__":
    app.run(debug=True)