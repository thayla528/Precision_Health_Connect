import os

from flask import Flask
import sys

from routes.auth import auth_bp
from routes.web import web_bp
from routes.api import api_bp

from routes.auth import login_manager

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "dev-key-segura")

from flask_wtf.csrf import CSRFProtect
csrf = CSRFProtect()
csrf.init_app(app)

login_manager.init_app(app)
login_manager.login_view = "auth.login"

# Blueprints
app.register_blueprint(auth_bp)
app.register_blueprint(web_bp)
app.register_blueprint(auth_bp)
app.register_blueprint(api_bp)

app.config.update(
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SECURE=False,  # True quando usar HTTPS
    SESSION_COOKIE_SAMESITE="Lax"
)

print(sys.executable)

API_URL = "http://127.0.0.1:5000"

DESVIAR_PROXY = {"http": None, "https": None}


# ------------------ RODAR ------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)