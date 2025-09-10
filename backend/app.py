from flask import Flask
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from mongoengine import connect
from config import Config

from routes.auth import auth
from routes.auth import register as auth_register
from routes.auth import login as auth_login
from routes.notes import notes
from routes.equipment import equipment_bp

app = Flask(__name__)
app.config.from_object(Config)

# Init Extensions
CORS(app, resources={r"/api/*": {"origins": "*"}})
jwt = JWTManager(app)

# MongoDB connect (รองรับทั้ง local และ Atlas)
if "uri" in app.config["MONGODB_SETTINGS"]:
    connect(host=app.config["MONGODB_SETTINGS"]["uri"])
else:
    connect(
        db=app.config["MONGODB_SETTINGS"]["db"],
        host=app.config["MONGODB_SETTINGS"]["host"],
        port=app.config["MONGODB_SETTINGS"]["port"]
    )

# Register Blueprints
app.register_blueprint(auth, url_prefix="/auth")
app.register_blueprint(notes, url_prefix="/api")
app.register_blueprint(equipment_bp, url_prefix="/api")

@app.route("/api/register", methods=["POST"])
def api_register():
    return auth_register()

@app.route("/api/login", methods=["POST"])
def api_login():
    return auth_login()

if __name__ == "__main__":
    app.run(debug=True)
