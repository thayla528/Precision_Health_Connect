import os
import sys

from flask import Flask
from flask_wtf.csrf import CSRFProtect

from routes.web import web_bp
from routes.auth import auth_bp


app = Flask(__name__)


app.secret_key = os.getenv(
    "SECRET_KEY",
    "dev-key-segura"
)


# ---------------- CSRF ----------------

csrf = CSRFProtect()



csrf.init_app(app)

csrf.exempt(auth_bp)


# ---------------- BLUEPRINTS ----------------

app.register_blueprint(web_bp)

app.register_blueprint(auth_bp)


# ---------------- SECURITY CONFIG ----------------

app.config.update(
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SECURE=False,
    SESSION_COOKIE_SAMESITE="Lax"
)


# ---------------- DEBUG ----------------

print(sys.executable)


# ---------------- RUN ----------------

if __name__ == "__main__":

    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )