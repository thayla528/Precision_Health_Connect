
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

@auth_bp.route(
    "/register",
    methods=["GET", "POST"]
)
def register():

    if request.method == "POST":

        invitation_code = request.form.get(
            "invitation_code"
        )

        password = request.form.get(
            "password"
        )

        confirm_password = request.form.get(
            "confirm_password"
        )


        # =================================================
        # VALIDAR CAMPOS
        # =================================================

        if not invitation_code or not password or not confirm_password:

            flash(
                "Todos os campos são obrigatórios.",
                "warning"
            )

            return redirect(
                url_for("auth.register")
            )


        # =================================================
        # VALIDAR SENHAS
        # =================================================

        if password != confirm_password:

            flash(
                "As senhas não coincidem.",
                "warning"
            )

            return redirect(
                url_for("auth.register")
            )


        # =================================================
        # ENVIAR PARA API
        # =================================================

        try:

            response = requests.post(

                f"{API_URL}/api/register",

                json={
                    "invitation_code": invitation_code,
                    "password": password
                },

                timeout=10
            )


        except requests.RequestException as e:

            print(
                "ERRO AO CONECTAR COM API:",
                e
            )

            flash(
                "Não foi possível conectar ao servidor.",
                "danger"
            )

            return redirect(
                url_for("auth.register")
            )


        # =================================================
        # DEBUG
        # =================================================

        print(
            "STATUS API:",
            response.status_code
        )

        print(
            "RESPOSTA API:",
            response.text
        )


        # =================================================
        # CONVERTER RESPOSTA
        # =================================================

        try:

            result = response.json()

        except ValueError:

            flash(
                "A API retornou uma resposta inválida.",
                "danger"
            )

            return redirect(
                url_for("auth.register")
            )


        # =================================================
        # CADASTRO REALIZADO
        # =================================================

        if response.status_code == 201 and result.get("success"):

            flash(
                result.get(
                    "message",
                    "Conta criada com sucesso!"
                ),
                "success"
            )

            return redirect(
                url_for("auth.login")
            )


        # =================================================
        # ERRO NO CADASTRO
        # =================================================

        flash(
            result.get(
                "message",
                "Não foi possível finalizar o cadastro."
            ),
            "danger"
        )


    return render_template(
        "user_registration.html"
    )


# =====================================================
# LOGIN
# =====================================================

@auth_bp.route(
    "/login",
    methods=["GET", "POST"]
)
def login():

    if request.method == "POST":

        email = request.form.get(
            "email"
        )

        password = request.form.get(
            "password"
        )


        # =================================================
        # ENVIAR PARA API
        # =================================================

        try:

            response = requests.post(

                f"{API_URL}/login",

                json={
                    "email": email,
                    "password": password
                },

                timeout=10
            )


        except requests.RequestException as e:

            print(
                "ERRO AO CONECTAR COM API:",
                e
            )

            flash(
                "Não foi possível conectar ao servidor.",
                "danger"
            )

            return render_template(
                "login.html"
            )


        # =================================================
        # DEBUG
        # =================================================

        print(
            "STATUS API:",
            response.status_code
        )

        print(
            "RESPOSTA API:",
            response.text
        )


        # =================================================
        # CONVERTER RESPOSTA
        # =================================================

        try:

            result = response.json()

        except ValueError:

            flash(
                "A API retornou uma resposta inválida.",
                "danger"
            )

            return render_template(
                "login.html"
            )


        # =================================================
        # LOGIN REALIZADO
        # =================================================

        if result.get("success"):

            user = result.get(
                "user"
            )


            if not user:

                flash(
                    "Dados do usuário não foram retornados pela API.",
                    "danger"
                )

                return render_template(
                    "login.html"
                )


            session["user_id"] = user["id"]

            session["user_name"] = user["full_name"]

            session["user_email"] = user["email"]

            session["role"] = user["role"]

            session["profile_type"] = user["profile_type"]


            flash(
                f"Bem-vindo(a), {session['user_name']}!",
                "success"
            )


            # =================================================
            # ADMINISTRADOR
            # =================================================

            if session["role"] == "administrator":

                return redirect(
                    url_for(
                        "web.admin_invitations"
                    )
                )


            # =================================================
            # PACIENTE
            # =================================================

            elif session["role"] == "patient":

                return redirect(
                    url_for(
                        "web.patient_dashboard"
                    )
                )


            # =================================================
            # PROFISSIONAL
            # =================================================

            elif session["role"] == "professional":

                return redirect(
                    url_for(
                        "web.health_professional_zone"
                    )
                )


            # =================================================
            # ROLE INVÁLIDA
            # =================================================

            else:

                flash(
                    "Tipo de usuário inválido.",
                    "danger"
                )

                return redirect(
                    url_for("auth.login")
                )


        # =================================================
        # ERRO DE LOGIN
        # =================================================

        flash(
            result.get(
                "message",
                "E-mail ou senha inválidos."
            ),
            "danger"
        )


    return render_template(
        "login.html"
    )


# =====================================================
# LOGOUT
# =====================================================

@auth_bp.route(
    "/logout"
)
def logout():

    session.clear()


    flash(
        "Logout realizado com sucesso.",
        "info"
    )


    return redirect(
        url_for(
            "web.public_page"
        )
    )

