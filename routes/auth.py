
from flask_login import LoginManager, UserMixin
from flask import Flask, render_template, url_for, flash, redirect, request, jsonify, Blueprint

auth_bp = Blueprint("auth", __name__)




API_URL = "http://127.0.0.1:5001"

DESVIAR_PROXY = {"http": None, "https": None}

login_manager = LoginManager()



class UserSession(UserMixin):
    def __init__(self, id, nome=None):
        self.id = id
        self.nome = nome

@login_manager.user_loader
def load_user(user_id):
    if not user_id:
        return None

    # Resgata o nome do operador que foi guardado na sessão do Flask durante o login
    from flask import session
    nome_usuario = session.get('user_name', 'Operador FlashLog')

    # Retorna a sessão mantendo a autenticação por ID, mas injetando o Nome para o HTML
    return UserSession(id=user_id, nome=nome_usuario)

@auth_bp.route('/')
def home():
    return redirect(url_for('auth.public_page'))

@auth_bp.route('/public_page')
def public_page():
    return render_template('public_page.html')

@auth_bp.route('/login')
def login():
    return render_template('login.html')

@auth_bp.route('/invitation')
def invitation():
    return render_template('invitation.html')

@auth_bp.route('/user_registration')
def user_registration():
    return render_template('user_registration.html')
