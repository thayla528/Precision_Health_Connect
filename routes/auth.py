from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    session,
    flash
)

import requests

auth_bp = Blueprint(
    "auth",
    __name__
)

API_URL = "http://127.0.0.1:5001"


# =====================================================
# FINALIZAR CADASTRO
# =====================================================

@auth_bp.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        invitation_code = request.form["invitation_code"]
        password = request.form["password"]
        confirm_password = request.form["confirm_password"]

        if password != confirm_password:

            flash(
                "As senhas não coincidem.",
                "warning"
            )

            return redirect(
                url_for("auth.register")
            )

        response = requests.post(
            f"{API_URL}/api/register",
            json={
                "invitation_code": invitation_code,
                "password": password
            }
        )

        print("STATUS API:", response.status_code)
        print("RESPOSTA API:", response.text)

        result = response.json()

        if result["success"]:

            flash(
                "Cadastro realizado com sucesso!",
                "success"
            )

            return redirect(
                url_for("auth.login")
            )

        flash(
            result["message"],
            "danger"
        )

    return render_template(
        "user_registration.html"
    )


# =====================================================
# LOGIN
# =====================================================

@auth_bp.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        email = request.form["email"]
        password = request.form["password"]

        response = requests.post(
            f"{API_URL}/login",
            json={
                "email": email,
                "password": password
            }
        )

        try:
            print("STATUS API:", response.status_code)
            print("RESPOSTA API:", response.text)

            result = response.json()

        except Exception:

            flash(
                "A API retornou uma resposta inválida.",
                "danger"
            )

            return render_template(
                "login.html"
            )

        if result["success"]:

            session["user_id"] = result["user"]["id"]
            session["user_name"] = result["user"]["full_name"]
            session["user_email"] = result["user"]["email"]
            session["role"] = result["user"]["role"]
            session["profile_type"] = result["user"]["profile_type"]

            flash(
                f"Bem-vindo(a), {session['user_name']}!",
                "success"
            )

            if session["role"] == "administrator":

                return redirect(
                    url_for("web.admin_invitations")
                )

            elif session["role"] == "patient":

                return redirect(
                    url_for("web.patient_dashboard")
                )

            elif session["role"] == "professional":

                return redirect(
                    url_for("web.health_professional_zone")
                )

            else:

                flash(
                    "Tipo de usuário inválido.",
                    "danger"
                )

                return redirect(
                    url_for("auth.login")
                )

        flash(
            result["message"],
            "danger"
        )

    return render_template(
        "login.html"
    )


# =====================================================
# LOGOUT
# =====================================================

@auth_bp.route("/logout")
def logout():

    session.clear()

    flash(
        "Logout realizado com sucesso.",
        "info"
    )

    return redirect(
        url_for("web.public_page")
    )