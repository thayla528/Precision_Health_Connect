from click import style
from flask import Blueprint, render_template, request, flash, redirect, url_for, session, abort, jsonify
import requests

import math

web_bp = Blueprint("web", __name__)

@web_bp.before_request
def debug_web_request():

    print("========================================", flush=True)
    print("WEB REQUEST", flush=True)
    print("METHOD:", request.method, flush=True)
    print("PATH:", request.path, flush=True)
    print("JSON:", request.get_json(silent=True), flush=True)
    print("========================================", flush=True)

API_URL = "http://127.0.0.1:5001"   # coloque a porta da sua API

from routes.decorators import admin_required

class Pagination:

    def __init__(self, items, page, per_page, total):

        self.items = items
        self.page = page
        self.per_page = per_page
        self.total = total
        self.pages = math.ceil(total / per_page)


    def iter_pages(
        self,
        left_edge=2,
        right_edge=2,
        left_current=2,
        right_current=2
    ):

        last = 0

        for num in range(1, self.pages + 1):

            if (
                num <= left_edge
                or num > self.pages - right_edge
                or (
                    num >= self.page - left_current
                    and num <= self.page + right_current
                )
            ):

                if last + 1 != num:
                    yield None

                yield num

                last = num



@web_bp.route('/')
def home():
    return redirect(
        url_for('web.public_page')
    )




@web_bp.route("/api/password/forgot", methods=["POST"])
def web_password_forgot():

    print()
    print("====================================================")
    print("WEB -> API | RECUPERAÇÃO DE SENHA")
    print("====================================================")

    # -------------------------------------------------
    # RECEBER JSON DO NAVEGADOR
    # -------------------------------------------------

    data = request.get_json(silent=True)

    print(
        "DADOS RECEBIDOS DA WEB:",
        data,
        flush=True
    )

    if not data:

        return jsonify({
            "success": False,
            "message": "Dados não enviados."
        }), 400

    email = data.get("email")

    if not email:

        return jsonify({
            "success": False,
            "message": "E-mail é obrigatório."
        }), 400

    # -------------------------------------------------
    # ENVIAR PARA A API
    # -------------------------------------------------

    api_url = f"{API_URL}/api/password/forgot"

    print(
        "ENVIANDO PARA API:",
        api_url,
        flush=True
    )

    try:

        response = requests.post(

            api_url,

            json={
                "email": email
            },

            timeout=10
        )

    except requests.RequestException as e:

        print(
            "ERRO AO CONECTAR COM A API:",
            repr(e),
            flush=True
        )

        return jsonify({

            "success": False,

            "message":
                "Não foi possível conectar com a API."

        }), 503

    # -------------------------------------------------
    # DEBUG DA RESPOSTA
    # -------------------------------------------------

    print(
        "STATUS DA API:",
        response.status_code,
        flush=True
    )

    print(
        "RESPOSTA DA API:",
        response.text,
        flush=True
    )

    # -------------------------------------------------
    # CONVERTER RESPOSTA
    # -------------------------------------------------

    try:

        result = response.json()

    except ValueError:

        print(
            "API NÃO RETORNOU JSON.",
            flush=True
        )

        return jsonify({

            "success": False,

            "message":
                "A API retornou uma resposta inválida."

        }), 502

    # -------------------------------------------------
    # DEVOLVER RESPOSTA DA API PARA O NAVEGADOR
    # -------------------------------------------------

    return jsonify(result), response.status_code


# =====================================================
# REDEFINIÇÃO DE SENHA
# WEB -> API
# =====================================================

@web_bp.route("/api/password/reset", methods=["POST"])
def web_password_reset():

    print()
    print("====================================================")
    print("WEB -> API | REDEFINIÇÃO DE SENHA")
    print("====================================================")

    # -------------------------------------------------
    # RECEBER JSON DO NAVEGADOR
    # -------------------------------------------------

    data = request.get_json(silent=True)

    print(
        "DADOS RECEBIDOS DA WEB:",
        data,
        flush=True
    )

    if not data:

        return jsonify({

            "success": False,

            "message":
                "Dados não enviados."

        }), 400

    reset_code = data.get("reset_code")

    new_password = data.get("new_password")

    confirm_password = data.get("confirm_password")

    # -------------------------------------------------
    # VALIDAÇÕES BÁSICAS
    # -------------------------------------------------

    if not reset_code:

        return jsonify({

            "success": False,

            "message":
                "Código de recuperação é obrigatório."

        }), 400

    if not new_password:

        return jsonify({

            "success": False,

            "message":
                "Nova senha é obrigatória."

        }), 400

    if not confirm_password:

        return jsonify({

            "success": False,

            "message":
                "Confirmação da senha é obrigatória."

        }), 400

    if new_password != confirm_password:

        return jsonify({

            "success": False,

            "message":
                "As senhas não coincidem."

        }), 400

    # -------------------------------------------------
    # ENVIAR PARA A API
    # -------------------------------------------------

    api_url = f"{API_URL}/api/password/reset"

    print(
        "ENVIANDO PARA API:",
        api_url,
        flush=True
    )

    try:

        response = requests.post(

            api_url,

            json={

                "reset_code":
                    reset_code,

                "new_password":
                    new_password,

                "confirm_password":
                    confirm_password

            },

            timeout=10
        )

    except requests.RequestException as e:

        print(
            "ERRO AO CONECTAR COM A API:",
            repr(e),
            flush=True
        )

        return jsonify({

            "success": False,

            "message":
                "Não foi possível conectar com a API."

        }), 503

    # -------------------------------------------------
    # DEBUG DA RESPOSTA
    # -------------------------------------------------

    print(
        "STATUS DA API:",
        response.status_code,
        flush=True
    )

    print(
        "RESPOSTA DA API:",
        response.text,
        flush=True
    )

    # -------------------------------------------------
    # CONVERTER RESPOSTA
    # -------------------------------------------------

    try:

        result = response.json()

    except ValueError:

        print(
            "API NÃO RETORNOU JSON.",
            flush=True
        )

        return jsonify({

            "success": False,

            "message":
                "A API retornou uma resposta inválida."

        }), 502

    # -------------------------------------------------
    # DEVOLVER RESPOSTA DA API
    # -------------------------------------------------

    return jsonify(result), response.status_code





@web_bp.route('/public_page')
def public_page():
    return render_template(
        'public_page.html'
    )


@web_bp.route('/login')
def login():
    return render_template(
        'login.html'
    )



@web_bp.route("/invitations/<int:id>")
def view_invitation(id):

    print("ID:", id)

    response = requests.get(
        f"{API_URL}/invitations/{id}"
    )

    print("STATUS:", response.status_code)
    print("BODY:", response.text)

    if response.status_code != 200:
        flash("Convite não encontrado.")
        return redirect(url_for("web.admin_invitations"))

    flash("Detalhes do convite carregados com sucesso.", "info")

    invitation = response.json()

    return render_template(
        "admin/invitation_details.html",
        invitation=invitation
    )

@web_bp.route(
    "/admin/invitations/<int:id>/reject",
    methods=["POST"]
)
def reject_invitation(id):

    response = requests.post(
        f"{API_URL}/admin/invitations/{id}/reject"
    )

    data = response.json()

    flash(
        data.get(
            "message",
            "Erro ao rejeitar convite."
        )
    )

    return redirect(
        url_for("web.admin_invitations")
    )



def approve_invitation(id):

    response = requests.post(
        f"{API_URL}/admin/invitations/{id}/approve"
    )

    data = response.json()

    flash(
        data.get(
            "message",
            "Erro ao aprovar convite."
        )
    )

    return redirect(
        url_for("web.admin_invitations")
    )



@web_bp.route(
    "/admin/invitations/<int:id>/approve",
    methods=["POST"]
)
def approve_invitation(id):

    response = requests.post(
        f"{API_URL}/admin/invitations/{id}/approve"
    )

    data = response.json()

    flash(
        data.get(
            "message",
            "Erro ao aprovar convite."
        )
    )

    return redirect(
        url_for("web.admin_invitations")
    )



@web_bp.route("/admin/invitations")
@admin_required
def admin_invitations():

    page = request.args.get(
        "page",
        1,
        type=int
    )

    per_page = 5

    search = request.args.get(
        "search",
        ""
    )

    status = request.args.get(
        "status",
        "todos"
    )


    # =========================
    # Busca API
    # =========================

    response = requests.get(
        f"{API_URL}/api/invitations"
    )


    if response.status_code != 200:

        flash(
            "Erro ao carregar convites.",
            "danger"
        )

        return render_template(
            "admin/admin_invitations.html",
            invitations=[],
            pending=0,
            approved=0,
            rejected=0,
            pagination=None
        )


    data = response.json()

    all_invitations = data["invitations"]


    # =========================
    # Cards
    # =========================

    pending = len(
        [
            i for i in all_invitations
            if i["status"] == "pending"
        ]
    )


    approved = len(
        [
            i for i in all_invitations
            if i["status"] == "approved"
        ]
    )


    rejected = len(
        [
            i for i in all_invitations
            if i["status"] == "rejected"
        ]
    )


    # =========================
    # Busca
    # =========================

    invitations = all_invitations


    if search:

        search_lower = search.lower()

        invitations = [
            i for i in invitations
            if search_lower in i["full_name"].lower()
            or search_lower in i["email"].lower()
        ]


    # =========================
    # Filtro status
    # =========================

    if status != "todos":

        invitations = [
            i for i in invitations
            if i["status"] == status
        ]


    # =========================
    # Paginação
    # =========================

    total = len(invitations)

    start = (page - 1) * per_page

    end = start + per_page


    paginated_invitations = invitations[start:end]

    pagination = Pagination(
        paginated_invitations,
        page,
        per_page,
        total
    )


    return render_template(
        "admin/admin_invitations.html",
        invitations=paginated_invitations,
        pending=pending,
        approved=approved,
        rejected=rejected,
        pagination=pagination,
        search=search,
        status=status
    )

@web_bp.route("/patient/exams")
def exams():

    return render_template(
        "patient/exams.html"
    )


@web_bp.route("/admin/users")
def users():

    # =====================================================
    # VERIFICAR AUTENTICAÇÃO
    # =====================================================

    if "user_id" not in session:

        return redirect(
            url_for("auth.login")
        )


    # =====================================================
    # VERIFICAR PERMISSÃO
    # =====================================================

    if session.get("role") != "administrator":

        abort(403)


    # =====================================================
    # PEGAR TOKEN JWT
    # =====================================================

    access_token = session.get(
        "access_token"
    )


    if not access_token:

        flash(
            "Sessão de autenticação expirada. Faça login novamente.",
            "warning"
        )

        session.clear()

        return redirect(
            url_for("auth.login")
        )


    # =====================================================
    # PEGAR FILTROS DA WEB
    # =====================================================

    search = request.args.get(
        "search",
        "",
        type=str
    ).strip()

    status = request.args.get(
        "status",
        "",
        type=str
    ).strip()

    page = request.args.get(
        "page",
        1,
        type=int
    )


    # =====================================================
    # GARANTIR PÁGINA VÁLIDA
    # =====================================================

    if page < 1:
        page = 1


    # =====================================================
    # HEADERS JWT
    # =====================================================

    headers = {

        "Authorization":
            f"Bearer {access_token}"

    }


    # =====================================================
    # CONSUMIR API
    # =====================================================

    try:

        response = requests.get(

            f"{API_URL}/users/active",

            headers=headers,

            timeout=10

        )


    except requests.RequestException as e:

        print(
            "ERRO AO CONECTAR COM API DE USUÁRIOS:",
            repr(e),
            flush=True
        )

        flash(
            "Não foi possível conectar ao servidor.",
            "danger"
        )

        return render_template(

            "admin/users.html",

            administrators=[],

            pagination=None,

            search=search,

            status=status

        )


    # =====================================================
    # DEBUG
    # =====================================================

    print(
        "STATUS API USUÁRIOS:",
        response.status_code,
        flush=True
    )

    print(
        "RESPOSTA API USUÁRIOS:",
        response.text,
        flush=True
    )


    # =====================================================
    # TOKEN INVÁLIDO / EXPIRADO
    # =====================================================

    if response.status_code in [401, 422]:

        session.clear()

        flash(
            "Sua sessão expirou. Faça login novamente.",
            "warning"
        )

        return redirect(
            url_for("auth.login")
        )


    # =====================================================
    # CONVERTER RESPOSTA
    # =====================================================

    try:

        result = response.json()

    except ValueError:

        flash(
            "A API retornou uma resposta inválida.",
            "danger"
        )

        return render_template(

            "admin/users.html",

            administrators=[],

            pagination=None,

            search=search,

            status=status

        )


    # =====================================================
    # ERRO DA API
    # =====================================================

    if not response.ok or not result.get("success"):

        flash(

            result.get(
                "message",
                "Não foi possível carregar os usuários."
            ),

            "danger"

        )

        return render_template(

            "admin/users.html",

            administrators=[],

            pagination=None,

            search=search,

            status=status

        )


    # =====================================================
    # DADOS VINDOS DA API
    # =====================================================

    users = result.get(
        "users",
        []
    )


    # =====================================================
    # BUSCA
    # =====================================================

    if search:

        search_lower = search.lower()

        users = [

            user
            for user in users

            if (

                search_lower
                in str(
                    user.get(
                        "full_name",
                        ""
                    )
                ).lower()

            )

            or (

                search_lower
                in str(
                    user.get(
                        "email",
                        ""
                    )
                ).lower()

            )

            or (

                search_lower
                in str(
                    user.get(
                        "role",
                        ""
                    )
                ).lower()

            )

        ]


    # =====================================================
    # FILTRO DE STATUS
    # =====================================================

    if status:

        status_lower = status.lower()

        users = [

            user
            for user in users

            if str(
                user.get(
                    "active",
                    ""
                )
            ).lower() == status_lower

        ]


    # =====================================================
    # PAGINAÇÃO LOCAL
    # =====================================================

    per_page = 10

    total = len(users)

    start = (
        page - 1
    ) * per_page

    end = start + per_page

    paginated_users = users[
        start:end
    ]


    # =====================================================
    # OBJETO DE PAGINAÇÃO
    # =====================================================

    pagination = Pagination(

        paginated_users,

        page,

        per_page,

        total

    )


    # =====================================================
    # ENVIAR PARA O TEMPLATE
    # =====================================================

    return render_template(

        "admin/users.html",

        administrators=paginated_users,

        pagination=pagination,

        search=search,

        status=status

    )

@web_bp.route("/admin/logs", methods=["GET"])
@admin_required
def logs():

    # =====================================================
    # VERIFICAR AUTENTICAÇÃO
    # =====================================================

    if "user_id" not in session:
        return redirect(
            url_for("auth.login")
        )

    # =====================================================
    # VERIFICAR PERMISSÃO
    # =====================================================

    if session.get("role") != "administrator":
        abort(403)

    # =====================================================
    # PEGAR TOKEN JWT
    # =====================================================

    access_token = session.get("access_token")

    if not access_token:

        flash(
            "Sessão de autenticação expirada. Faça login novamente.",
            "warning"
        )

        session.clear()

        return redirect(
            url_for("auth.login")
        )

    # =====================================================
    # FILTROS
    # =====================================================

    search = request.args.get(
        "search",
        "",
        type=str
    )

    action = request.args.get(
        "action",
        "",
        type=str
    )

    page = request.args.get(
        "page",
        1,
        type=int
    )

    if page < 1:
        page = 1

    # =====================================================
    # HEADERS
    # =====================================================

    headers = {
        "Authorization": f"Bearer {access_token}"
    }

    # =====================================================
    # PARÂMETROS
    # =====================================================

    params = {
        "page": page,
        "per_page": 10
    }

    if search:
        params["search"] = search

    if action:
        params["action"] = action

    # =====================================================
    # CONSUMIR API
    # =====================================================

    try:

        response = requests.get(
            f"{API_URL}/admin/logs",
            headers=headers,
            params=params,
            timeout=10
        )

    except requests.RequestException as e:

        print(
            "ERRO AO CONECTAR COM API DE AUDITORIA:",
            repr(e),
            flush=True
        )

        flash(
            "Não foi possível conectar ao servidor.",
            "danger"
        )

        return render_template(
            "admin/logs.html",
            logs=[],
            pagination=None,
            search=search,
            action=action
        )

    # =====================================================
    # DEBUG
    # =====================================================

    print(
        "STATUS API AUDIT LOGS:",
        response.status_code,
        flush=True
    )

    print(
        "RESPOSTA API AUDIT LOGS:",
        response.text,
        flush=True
    )

    # =====================================================
    # TOKEN EXPIRADO
    # =====================================================

    if response.status_code in [401, 422]:

        session.clear()

        flash(
            "Sua sessão expirou. Faça login novamente.",
            "warning"
        )

        return redirect(
            url_for("auth.login")
        )

    # =====================================================
    # JSON
    # =====================================================

    try:

        result = response.json()

    except ValueError:

        flash(
            "A API retornou uma resposta inválida.",
            "danger"
        )

        return render_template(
            "admin/logs.html",
            logs=[],
            pagination=None,
            search=search,
            action=action
        )

    # =====================================================
    # ERRO DA API
    # =====================================================

    if not response.ok or not result.get("success"):

        flash(
            result.get(
                "message",
                "Não foi possível carregar os logs."
            ),
            "danger"
        )

        return render_template(
            "admin/logs.html",
            logs=[],
            pagination=None,
            search=search,
            action=action
        )

    # =====================================================
    # LOGS
    # =====================================================

    logs_data = result.get(
        "logs",
        []
    )

    # =====================================================
    # PAGINAÇÃO
    # =====================================================

    pagination_data = result.get(
        "pagination",
        {}
    )

    pagination = Pagination(
        logs_data,
        pagination_data.get("page", page),
        pagination_data.get("per_page", 10),
        pagination_data.get("total", 0)
    )

    # =====================================================
    # TEMPLATE
    # =====================================================

    return render_template(
        "admin/logs.html",
        logs=logs_data,
        pagination=pagination,
        search=search,
        action=action
    )
@web_bp.route("/admin/admin", methods=["GET", "POST"])
@admin_required
def admin():

    # =====================================================
    # VERIFICAR TOKEN JWT
    # =====================================================

    token = session.get("access_token")

    if not token:

        flash(
            "Sessão expirada. Faça login novamente.",
            "danger"
        )

        return redirect(
            url_for("auth.login")
        )

    # =====================================================
    # HEADERS
    # =====================================================

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    # =====================================================
    # POST
    # =====================================================

    if request.method == "POST":

        action = request.form.get("action")

        target_id = request.form.get(
            "administrator_id"
        )

        # =================================================
        # CRIAR CONVITE DE ADMINISTRADOR
        # =================================================

        if action == "create_admin":

            full_name = request.form.get(
                "full_name",
                ""
            ).strip()

            email = request.form.get(
                "email",
                ""
            ).strip()

            phone = request.form.get(
                "phone",
                ""
            ).strip()

            # =============================================
            # VALIDAÇÃO
            # =============================================

            if not full_name:

                flash(
                    "Informe o nome completo.",
                    "danger"
                )

                return redirect(
                    url_for("web.admin")
                )

            if not email:

                flash(
                    "Informe o e-mail.",
                    "danger"
                )

                return redirect(
                    url_for("web.admin")
                )

            # =============================================
            # CONSUMIR API
            # =============================================

            api_url_create = (
                f"{API_URL}/administrators"
            )

            try:

                response = requests.post(

                    api_url_create,

                    json={
                        "full_name": full_name,
                        "email": email,
                        "phone": phone,
                        "profile_photo": None
                    },

                    headers=headers,

                    timeout=10

                )

            except requests.RequestException as e:

                print(
                    "ERRO AO CRIAR CONVITE DE ADMINISTRADOR:",
                    repr(e),
                    flush=True
                )

                flash(
                    "Não foi possível conectar ao servidor.",
                    "danger"
                )

                return redirect(
                    url_for("web.admin")
                )

            # =============================================
            # TOKEN EXPIRADO
            # =============================================

            if response.status_code in [401, 422]:

                session.clear()

                flash(
                    "Sua sessão expirou. Faça login novamente.",
                    "warning"
                )

                return redirect(
                    url_for("auth.login")
                )

            # =============================================
            # PROCESSAR JSON
            # =============================================

            try:

                result = response.json()

            except ValueError:

                print(
                    "RESPOSTA INVÁLIDA DA API:",
                    response.text,
                    flush=True
                )

                flash(
                    "A API retornou uma resposta inválida.",
                    "danger"
                )

                return redirect(
                    url_for("web.admin")
                )

            # =============================================
            # SUCESSO
            # =============================================

            if response.status_code == 201 and result.get("success"):

                flash(
                    "Administrador adicionado. "
                    "O código do convite foi enviado por e-mail.",
                    "success"
                )

            # =============================================
            # ERRO
            # =============================================

            else:

                flash(
                    result.get(
                        "message",
                        "Erro ao criar administrador."
                    ),
                    "danger"
                )

        # =================================================
        # DESATIVAR ADMINISTRADOR
        # =================================================

        elif action == "deactivate":

            api_url_deactivate = (
                f"{API_URL}/administrators/"
                f"{target_id}/deactivate"
            )

            try:

                response = requests.put(

                    api_url_deactivate,

                    headers=headers,

                    timeout=10

                )

                if response.status_code in [401, 422]:

                    session.clear()

                    flash(
                        "Sua sessão expirou. Faça login novamente.",
                        "warning"
                    )

                    return redirect(
                        url_for("auth.login")
                    )

                result = response.json()

                if (
                    response.status_code == 200
                    and result.get("success")
                ):

                    flash(
                        "Administrador desativado com sucesso!",
                        "success"
                    )

                else:

                    flash(
                        result.get(
                            "message",
                            "Erro ao desativar administrador."
                        ),
                        "danger"
                    )

            except requests.RequestException as e:

                print(
                    "ERRO AO DESATIVAR ADMINISTRADOR:",
                    repr(e),
                    flush=True
                )

                flash(
                    "Erro de conexão ao tentar desativar o administrador.",
                    "danger"
                )

        # =================================================
        # ATIVAR ADMINISTRADOR
        # =================================================

        elif action == "activate":

            api_url_activate = (
                f"{API_URL}/administrators/"
                f"{target_id}/activate"
            )

            try:

                response = requests.put(

                    api_url_activate,

                    headers=headers,

                    timeout=10

                )

                if response.status_code in [401, 422]:

                    session.clear()

                    flash(
                        "Sua sessão expirou. Faça login novamente.",
                        "warning"
                    )

                    return redirect(
                        url_for("auth.login")
                    )

                result = response.json()

                if (
                    response.status_code == 200
                    and result.get("success")
                ):

                    flash(
                        "Administrador ativado com sucesso!",
                        "success"
                    )

                else:

                    flash(
                        result.get(
                            "message",
                            "Erro ao ativar administrador."
                        ),
                        "danger"
                    )

            except requests.RequestException as e:

                print(
                    "ERRO AO ATIVAR ADMINISTRADOR:",
                    repr(e),
                    flush=True
                )

                flash(
                    "Erro de conexão ao tentar ativar o administrador.",
                    "danger"
                )

        # =================================================
        # REDIRECT
        # =================================================

        return redirect(
            url_for("web.admin")
        )

    # =====================================================
    # GET
    # =====================================================

    search = request.args.get(
        "search",
        default="",
        type=str
    )

    status = request.args.get(
        "status",
        default="",
        type=str
    )

    page = request.args.get(
        "page",
        default=1,
        type=int
    )

    per_page = request.args.get(
        "per_page",
        default=10,
        type=int
    )

    # =====================================================
    # PARÂMETROS
    # =====================================================

    params = {
        "page": page,
        "per_page": per_page
    }

    if search.strip():

        params["search"] = search.strip()

    if status.strip():

        params["status"] = status.strip()

    # =====================================================
    # LISTAR ADMINISTRADORES
    # =====================================================

    api_url_list = (
        f"{API_URL}/administrators"
    )

    administrators_list = []

    pagination = Pagination(
        [],
        page,
        per_page,
        0
    )

    try:

        response = requests.get(

            api_url_list,

            params=params,

            headers=headers,

            timeout=10

        )

        # =============================================
        # TOKEN EXPIRADO
        # =============================================

        if response.status_code in [401, 422]:

            session.clear()

            flash(
                "Sua sessão expirou. Faça login novamente.",
                "warning"
            )

            return redirect(
                url_for("auth.login")
            )

        # =============================================
        # SUCESSO
        # =============================================

        if response.status_code == 200:

            result = response.json()

            if result.get("success"):

                administrators_list = result.get(
                    "administrators",
                    []
                )

                pag_data = result.get(
                    "pagination",
                    {}
                )

                pagination = Pagination(

                    items=administrators_list,

                    page=pag_data.get(
                        "page",
                        page
                    ),

                    per_page=pag_data.get(
                        "per_page",
                        per_page
                    ),

                    total=pag_data.get(
                        "total",
                        0
                    )

                )

            else:

                flash(
                    result.get(
                        "message",
                        "Erro ao carregar administradores."
                    ),
                    "danger"
                )

        else:

            try:

                result = response.json()

                flash(
                    result.get(
                        "message",
                        "Erro ao carregar administradores."
                    ),
                    "danger"
                )

            except ValueError:

                flash(
                    "Resposta inválida do servidor.",
                    "danger"
                )

    except requests.RequestException as e:

        print(
            "ERRO AO LISTAR ADMINISTRADORES:",
            repr(e),
            flush=True
        )

        flash(
            "Não foi possível conectar ao servidor de dados.",
            "danger"
        )

    # =====================================================
    # TEMPLATE
    # =====================================================

    return render_template(

        "admin/admin.html",

        administrators=administrators_list,

        pagination=pagination,

        search=search,

        status=status

    )

@web_bp.route("/api/administrators/<int:administrator_id>", methods=["GET"])
@admin_required
def web_get_administrator_details(administrator_id):
    token = session.get("access_token")
    if not token:
        return jsonify({"success": False, "message": "Sessão expirada."}), 401

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    # Faz a busca segura por dentro do servidor (Porta 5001)
    api_url = f"{API_URL}/administrators/{administrator_id}"
    try:
        response = requests.get(api_url, headers=headers, timeout=10)
        return jsonify(response.json()), response.status_code
    except requests.RequestException:
        return jsonify({"success": False, "message": "Erro de conexão com a API."}), 503

@web_bp.route("/admin/profile", methods=["GET", "POST"])
@admin_required
def profiles():  # Sincronizado no plural para bater com o url_for('web.profiles') do base.html
    token = session.get("access_token")
    user_id = session.get("user_id") or session.get("id")

    if not token or not user_id:
        flash("Sessão expirada. Faça login novamente.", "danger")
        return redirect(url_for("auth.login"))

    # O requests define o Content-Type correto com o boundary automaticamente ao usar o parâmetro 'files'.
    headers = {
        "Authorization": f"Bearer {token}"
    }

    # =====================================================
    # PROCESSAMENTO DO SALVAMENTO (POST)
    # =====================================================
    if request.method == "POST":
        full_name = request.form.get("full_name")
        email = request.form.get("email")
        phone = request.form.get("phone")
        new_password = request.form.get("new_password")
        confirm_password = request.form.get("confirm_password")

        if new_password:
            if new_password != confirm_password:
                flash("A confirmação da nova senha não coincide.", "warning")
                return redirect(url_for("web.profiles"))
            password_to_send = new_password
        else:
            password_to_send = ""  # Enviamos vazio para indicar que não houve alteração de senha

        # 1. Prepara os campos de texto comuns (FormData para a API)
        payload = {
            "full_name": full_name,
            "email": email,
            "password": password_to_send,
            "phone": phone
        }

        # 2. Captura o arquivo de foto vindo do HTML e prepara o dicionário de arquivos
        files = {}
        if "profile_photo" in request.files:
            file = request.files["profile_photo"]
            if file and file.filename != "":
                # Passamos o arquivo diretamente para o requests com o nome do campo esperado pela API
                files = {"profile_photo": (file.filename, file.stream, file.mimetype)}
            else:
                # Se o usuário não enviou um arquivo novo, mantemos o valor atual da sessão
                payload["profile_photo"] = session.get("profile_photo", "")

        api_url_update = f"{API_URL}/administrators/{user_id}"
        try:
            # Enviamos usando data= (para textos) e files= (para arquivos)
            response = requests.put(
                api_url_update,
                data=payload,
                files=files if files else None,
                headers=headers,
                timeout=10
            )

            try:
                result = response.json()
                if response.status_code == 200 and result.get("success"):
                    session["user_name"] = full_name
                    session["user_email"] = email

                    # Sincronização: Atualiza a session do frontend com a string da nova foto retornada pela API
                    if "administrator" in result and "profile_photo" in result["administrator"]:
                        session["profile_photo"] = result["administrator"]["profile_photo"]

                    flash("Informações do perfil atualizadas com sucesso!", "success")
                else:
                    flash(result.get("message", "Erro ao atualizar perfil."), "danger")
            except ValueError:
                flash("A API retornou uma resposta inválida ao salvar.", "danger")

        except requests.RequestException:
            flash("Erro de conexão ao salvar alterações.", "danger")

        return redirect(url_for("web.profiles"))

    # =====================================================
    # CARREGAMENTO INICIAL DOS DADOS (GET)
    # =====================================================
    # Configuração inicial baseada nos dados da sessão atual
    admin_data = {
        "full_name": session.get("user_name", ""),
        "email": session.get("user_email", ""),
        "phone": "",
        "role": "Administrador",
        "created_at": "--",
        "last_login": "Nunca",
        "profile_photo": session.get("profile_photo", "")
    }

    # Mantemos o Content-Type original para a rota GET já que ela não envia arquivos binários
    headers_get = {**headers, "Content-Type": "application/json"}
    api_url_details = f"{API_URL}/administrators/{user_id}"
    try:
        response = requests.get(api_url_details, headers=headers_get, timeout=10)
        if response.status_code == 200:
            try:
                res_json = response.json()
                if res_json.get("success") and res_json.get("administrator"):
                    # Substitui os dados locais pelos dados reais vindos da API
                    admin_data = res_json.get("administrator")

                    # Sincronização Crítica: Garante que o template HTML tenha acesso ao arquivo guardado na API
                    if not admin_data.get("profile_photo"):
                        admin_data["profile_photo"] = session.get("profile_photo", "")
                    else:
                        session["profile_photo"] = admin_data["profile_photo"]
            except ValueError:
                print("Resposta da API de detalhes não continha um JSON válido.")
        else:
            print(f"API de detalhes retornou status HTTP {response.status_code}")

    except requests.RequestException as e:
        print("Erro de conexão ao buscar detalhes do perfil:", e)

    return render_template(
        "admin/profile.html",
        admin_data=admin_data
    )



@web_bp.route("/professional")
def health_professional_zone():

    if session.get("role") != "professional":
        abort(403)

    return redirect(
        url_for("web.health_professional_dashboard")
    )




@web_bp.route("/admin/settings")
def settings():
    return render_template(
        "admin/settings.html"
    )


# ============================
# DASHBOARD PROFISSIONAL
# ============================

@web_bp.route("/profession/health_professional_dashboard")
def health_professional_dashboard():

    if session.get("role") != "professional":
        abort(403)

    stats = {
        "total_patients": 0,
        "today_appointments": 0,
        "completed_appointments": 0,
        "pending_documents": 0
    }

    return render_template(
        "profession/health_professional_dashboard.html",
        stats=stats
    )

@web_bp.route(
    "/profession/patients/create",
    methods=["POST"]
)
def create_patient_link():

    # =====================================================
    # VERIFICAR AUTENTICAÇÃO / PERFIL
    # =====================================================

    if session.get("role") != "professional":

        return jsonify({
            "success": False,
            "message": "Acesso não autorizado."
        }), 403


    # =====================================================
    # TOKEN JWT
    # =====================================================

    access_token = session.get(
        "access_token"
    )


    if not access_token:

        return jsonify({
            "success": False,
            "message": "Sessão expirada."
        }), 401


    # =====================================================
    # JSON
    # =====================================================

    data = request.get_json()


    if not data:

        return jsonify({
            "success": False,
            "message": "JSON body is required."
        }), 400


    patient_id = data.get(
        "patient_id"
    )


    professional_id = data.get(
        "professional_id"
    )


    if not patient_id or not professional_id:

        return jsonify({
            "success": False,
            "message":
                "patient_id and professional_id are required."
        }), 400


    # =====================================================
    # CONSUMIR API
    # =====================================================

    try:

        response = requests.post(

            f"{API_URL}/patient-professional/create",

            json={
                "patient_id": patient_id,
                "professional_id": professional_id
            },

            headers={
                "Authorization":
                    f"Bearer {access_token}",

                "Accept":
                    "application/json"
            },

            timeout=10
        )

    except requests.RequestException as e:

        print(
            "ERRO AO CONSUMIR API "
            "/patient-professional/create:",
            e
        )

        return jsonify({
            "success": False,
            "message":
                "Não foi possível conectar à API."
        }), 500


    # =====================================================
    # TOKEN INVÁLIDO
    # =====================================================

    if response.status_code in [401, 422]:

        session.clear()

        return jsonify({
            "success": False,
            "message": "Sessão expirada."
        }), 401


    # =====================================================
    # DEVOLVER RESPOSTA DA API
    # =====================================================

    try:

        result = response.json()

    except ValueError:

        return jsonify({
            "success": False,
            "message":
                "Resposta inválida da API."
        }), 500


    return jsonify(result), response.status_code

# =====================================================
# BUSCAR PACIENTES PARA ADICIONAR
# =====================================================

@web_bp.route("/profession/patients/search", methods=["GET"])
def professional_search_patients():

    # =====================================================
    # VERIFICAR AUTENTICAÇÃO / PERFIL
    # =====================================================

    if session.get("role") != "professional":
        return jsonify({
            "success": False,
            "message": "Acesso não autorizado."
        }), 403

    # =====================================================
    # TOKEN JWT
    # =====================================================

    access_token = session.get("access_token")

    if not access_token:
        return jsonify({
            "success": False,
            "message": "Sessão expirada."
        }), 401

    # =====================================================
    # TERMO DE BUSCA
    # =====================================================

    search = request.args.get(
        "search",
        ""
    ).strip()

    # =====================================================
    # CONSUMIR API
    # =====================================================

    try:

        response = requests.get(
            f"{API_URL}/patient-professional/patients/search",
            params={
                "search": search
            },
            headers={
                "Authorization": f"Bearer {access_token}",
                "Accept": "application/json"
            },
            timeout=10
        )

    except requests.RequestException as e:

        print(
            "ERRO AO CONSUMIR API "
            "/patient-professional/patients/search:",
            e
        )

        return jsonify({
            "success": False,
            "message": "Não foi possível conectar à API."
        }), 500

    # =====================================================
    # TOKEN INVÁLIDO / EXPIRADO
    # =====================================================

    if response.status_code in [401, 422]:

        session.clear()

        return jsonify({
            "success": False,
            "message": "Sessão expirada."
        }), 401

    # =====================================================
    # ACESSO NEGADO
    # =====================================================

    if response.status_code == 403:

        return jsonify({
            "success": False,
            "message": "Acesso não autorizado."
        }), 403

    # =====================================================
    # OUTRO ERRO
    # =====================================================

    if response.status_code != 200:

        print(
            "ERRO API /patient-professional/patients/search:",
            response.status_code,
            response.text
        )

        return jsonify({
            "success": False,
            "message": "Não foi possível buscar os pacientes."
        }), response.status_code

    # =====================================================
    # CONVERTER JSON
    # =====================================================

    try:

        data = response.json()

    except ValueError:

        return jsonify({
            "success": False,
            "message": "Resposta inválida da API."
        }), 500

    # =====================================================
    # DEVOLVER RESPOSTA PARA O HTML
    # =====================================================

    return jsonify(data), 200
# =========================================================
# PÁGINA DE PACIENTES DO PROFISSIONAL
# =========================================================

@web_bp.route("/profession/patients")
def professional_patients():

    # =====================================================
    # VERIFICAR AUTENTICAÇÃO / PERFIL
    # =====================================================

    if session.get("role") != "professional":
        abort(403)

    # =====================================================
    # TOKEN JWT
    # =====================================================

    access_token = session.get("access_token")

    if not access_token:
        return redirect(url_for("web.login"))

    # =====================================================
    # BUSCAR PERFIL DO PROFESSIONAL
    # =====================================================

    try:

        profile_response = requests.get(
            f"{API_URL}/professional/profile",
            headers={
                "Authorization": f"Bearer {access_token}"
            },
            timeout=10
        )

    except requests.RequestException as e:

        print(
            "ERRO AO CONSUMIR API /professional/profile:",
            e
        )

        return render_template(
            "profession/professional_patients.html",
            patients=[],
            professional=None,
            professional_id=None,
            api_error="Não foi possível conectar à API."
        )

    # =====================================================
    # TOKEN INVÁLIDO / EXPIRADO
    # =====================================================

    if profile_response.status_code in [401, 422]:

        session.clear()

        return redirect(
            url_for("web.login")
        )

    # =====================================================
    # ACESSO NEGADO
    # =====================================================

    if profile_response.status_code == 403:

        return render_template(
            "profession/professional_patients.html",
            patients=[],
            professional=None,
            professional_id=None,
            api_error="Acesso não autorizado."
        )

    # =====================================================
    # OUTRO ERRO
    # =====================================================

    if profile_response.status_code != 200:

        print(
            "ERRO API /professional/profile:",
            profile_response.status_code,
            profile_response.text
        )

        return render_template(
            "profession/professional_patients.html",
            patients=[],
            professional=None,
            professional_id=None,
            api_error="Não foi possível carregar o perfil profissional."
        )

    # =====================================================
    # CONVERTER RESPOSTA
    # =====================================================

    try:

        profile_data = profile_response.json()

    except ValueError:

        return render_template(
            "profession/professional_patients.html",
            patients=[],
            professional=None,
            professional_id=None,
            api_error="Resposta inválida da API."
        )

    # =====================================================
    # VALIDAR PERFIL
    # =====================================================

    if not profile_data.get("success"):

        return render_template(
            "profession/professional_patients.html",
            patients=[],
            professional=None,
            professional_id=None,
            api_error=profile_data.get(
                "message",
                "Não foi possível carregar o perfil."
            )
        )

    professional = profile_data.get(
        "professional"
    )

    if not professional:

        return render_template(
            "profession/professional_patients.html",
            patients=[],
            professional=None,
            professional_id=None,
            api_error="Perfil profissional não encontrado."
        )

    # =====================================================
    # ID DO PROFESSIONAL
    # =====================================================

    professional_id = professional.get(
        "id"
    )

    if not professional_id:

        return render_template(
            "profession/professional_patients.html",
            patients=[],
            professional=professional,
            professional_id=None,
            api_error="ID do profissional não encontrado."
        )

    # =====================================================
    # BUSCAR PACIENTES VINCULADOS
    # =====================================================

    try:

        patients_response = requests.get(

            f"{API_URL}/patient-professional/"
            f"professional/{professional_id}/patients",

            headers={
                "Authorization":
                    f"Bearer {access_token}"
            },

            timeout=10
        )

    except requests.RequestException as e:

        print(
            "ERRO AO CONSUMIR API "
            "/patient-professional/professional/.../patients:",
            e
        )

        return render_template(
            "profession/professional_patients.html",
            patients=[],
            professional=professional,
            professional_id=professional_id,
            api_error="Não foi possível carregar os pacientes."
        )

    # =====================================================
    # TOKEN INVÁLIDO / EXPIRADO
    # =====================================================

    if patients_response.status_code in [401, 422]:

        session.clear()

        return redirect(
            url_for("web.login")
        )

    # =====================================================
    # ACESSO NEGADO
    # =====================================================

    if patients_response.status_code == 403:

        print(
            "403 AO BUSCAR PACIENTES:",
            patients_response.text
        )

        return render_template(
            "profession/professional_patients.html",
            patients=[],
            professional=professional,
            professional_id=professional_id,
            api_error="Acesso não autorizado aos pacientes."
        )

    # =====================================================
    # OUTRO ERRO
    # =====================================================

    if patients_response.status_code != 200:

        print(
            "ERRO API PACIENTES:",
            patients_response.status_code,
            patients_response.text
        )

        return render_template(
            "profession/professional_patients.html",
            patients=[],
            professional=professional,
            professional_id=professional_id,
            api_error="Não foi possível carregar os pacientes."
        )

    # =====================================================
    # CONVERTER JSON DOS PACIENTES
    # =====================================================

    try:

        patients_data = patients_response.json()

    except ValueError:

        return render_template(
            "profession/professional_patients.html",
            patients=[],
            professional=professional,
            professional_id=professional_id,
            api_error="Resposta inválida da API de pacientes."
        )

    # =====================================================
    # VALIDAR RESPOSTA
    # =====================================================

    if not patients_data.get("success"):

        return render_template(
            "profession/professional_patients.html",
            patients=[],
            professional=professional,
            professional_id=professional_id,
            api_error=patients_data.get(
                "message",
                "Não foi possível carregar os pacientes."
            )
        )

    # =====================================================
    # PACIENTES
    # =====================================================

    patients = patients_data.get(
        "relationships",
        []
    )

    # =====================================================
    # DEBUG
    # =====================================================

    print(
        "\n========= PROFESSIONAL PATIENTS ========="
    )

    print(
        "Professional ID:",
        professional_id
    )

    print(
        "Total de relacionamentos:",
        len(patients)
    )

    print(
        "Pacientes:",
        patients
    )

    print(
        "=========================================\n"
    )

    # =====================================================
    # RENDER
    # =====================================================

    return render_template(
        "profession/professional_patients.html",

        patients=patients,

        professional=professional,

        professional_id=professional_id,

        api_error=None
    )


# =========================================================
# BUSCAR PACIENTES PARA ADICIONAR
# =========================================================

@web_bp.route(
    "/profession/patients/search",
    methods=["GET"]
)
def search_patients():

    # =====================================================
    # VERIFICAR AUTENTICAÇÃO / PERFIL
    # =====================================================

    if session.get("role") != "professional":

        return jsonify({
            "success": False,
            "message": "Acesso não autorizado."
        }), 403

    # =====================================================
    # TOKEN JWT
    # =====================================================

    access_token = session.get(
        "access_token"
    )

    if not access_token:

        return jsonify({
            "success": False,
            "message": "Sessão expirada."
        }), 401

    # =====================================================
    # TERMO DE PESQUISA
    # =====================================================

    search = request.args.get(
        "search",
        ""
    ).strip()

    # =====================================================
    # CONSUMIR API
    # =====================================================

    try:

        response = requests.get(

            f"{API_URL}/patient-professional/"
            f"patients/search",

            params={
                "search": search
            },

            headers={
                "Authorization":
                    f"Bearer {access_token}",

                "Accept":
                    "application/json"
            },

            timeout=10
        )

    except requests.RequestException as e:

        print(
            "ERRO AO CONSUMIR API "
            "/patient-professional/patients/search:",
            e
        )

        return jsonify({
            "success": False,
            "message":
                "Não foi possível conectar à API."
        }), 500

    # =====================================================
    # TOKEN INVÁLIDO / EXPIRADO
    # =====================================================

    if response.status_code in [401, 422]:

        session.clear()

        return jsonify({
            "success": False,
            "message": "Sessão expirada."
        }), 401

    # =====================================================
    # ACESSO NEGADO
    # =====================================================

    if response.status_code == 403:

        return jsonify({
            "success": False,
            "message": "Acesso não autorizado."
        }), 403

    # =====================================================
    # OUTRO ERRO
    # =====================================================

    if response.status_code != 200:

        print(
            "ERRO API /patient-professional/"
            "patients/search:",

            response.status_code,

            response.text
        )

        return jsonify({
            "success": False,
            "message":
                "Não foi possível buscar os pacientes."
        }), response.status_code

    # =====================================================
    # CONVERTER JSON
    # =====================================================

    try:

        data = response.json()

    except ValueError:

        return jsonify({
            "success": False,
            "message":
                "Resposta inválida da API."
        }), 500

    # =====================================================
    # DEVOLVER RESPOSTA DA API
    # =====================================================

    return jsonify(data), 200




# ============================
# PRONTUÁRIO MÉDICO
# ============================

@web_bp.route("/profession/medical-record")
def professional_medical_record():

    if session.get("role") != "professional":
        abort(403)

    return render_template(
        "profession/professional_medical_record.html"
    )

@web_bp.route(
    "/profession/appointments/<int:appointment_id>/reschedule",
    methods=["PUT"]
)
def professional_reschedule_appointment(appointment_id):

    # =====================================================
    # VERIFICAR AUTENTICAÇÃO
    # =====================================================

    if "user_id" not in session:
        return jsonify({
            "success": False,
            "message": "Sessão expirada."
        }), 401

    # =====================================================
    # VERIFICAR PERMISSÃO
    # =====================================================

    if session.get("role") != "professional":
        return jsonify({
            "success": False,
            "message": "Acesso negado."
        }), 403

    # =====================================================
    # TOKEN
    # =====================================================

    access_token = session.get("access_token")

    if not access_token:

        session.clear()

        return jsonify({
            "success": False,
            "message": "Sessão expirada."
        }), 401

    # =====================================================
    # HEADERS
    # =====================================================

    headers = {
        "Authorization": f"Bearer {access_token}"
    }

    # =====================================================
    # CONSUMIR API
    # =====================================================

    try:

        response = requests.put(
            f"{API_URL}/appointments/{appointment_id}/reschedule",
            json=request.get_json(),
            headers=headers,
            timeout=10
        )

    except requests.RequestException as e:

        print(
            f"Erro ao conectar com API: {e}"
        )

        return jsonify({
            "success": False,
            "message": "Erro de conexão com a API."
        }), 500

    # =====================================================
    # TOKEN INVÁLIDO
    # =====================================================

    if response.status_code in [401, 422]:

        session.clear()

        return jsonify({
            "success": False,
            "message": "Sessão expirada."
        }), 401

    # =====================================================
    # JSON
    # =====================================================

    try:

        data = response.json()

    except ValueError:

        return jsonify({
            "success": False,
            "message": "Resposta inválida da API."
        }), 500

    return jsonify(data), response.status_code


@web_bp.route("/profession/appointments/data", methods=["GET"])
def professional_appointments_data():

    if "user_id" not in session:
        return jsonify({
            "success": False,
            "message": "Não autenticado."
        }), 401

    if session.get("role") != "professional":
        return jsonify({
            "success": False,
            "message": "Acesso negado."
        }), 403

    access_token = session.get("access_token")

    if not access_token:
        session.clear()

        return jsonify({
            "success": False,
            "message": "Sessão expirada."
        }), 401

    headers = {
        "Authorization": f"Bearer {access_token}"
    }

    try:

        response = requests.get(
            f"{API_URL}/appointments/my",
            headers=headers,
            timeout=10
        )

    except requests.RequestException as e:

        print(
            f"Erro ao conectar com API de appointments: {e}"
        )

        return jsonify({
            "success": False,
            "message": "Não foi possível conectar à API."
        }), 500

    if response.status_code in [401, 422]:

        session.clear()

        return jsonify({
            "success": False,
            "message": "Sessão expirada."
        }), 401

    if response.status_code != 200:

        print(
            "Erro API appointments:",
            response.status_code,
            response.text
        )

        return jsonify({
            "success": False,
            "message": "Não foi possível carregar as consultas."
        }), response.status_code

    try:

        data = response.json()

    except ValueError:

        return jsonify({
            "success": False,
            "message": "Resposta inválida da API."
        }), 500

    return jsonify(data), 200

@web_bp.route("/profession/calendar")
def professional_calendar():

    # =====================================================
    # VERIFICAR AUTENTICAÇÃO
    # =====================================================

    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    # =====================================================
    # VERIFICAR PERMISSÃO
    # =====================================================

    if session.get("role") != "professional":
        abort(403)

    # =====================================================
    # TOKEN JWT
    # =====================================================

    access_token = session.get("access_token")

    if not access_token:
        session.clear()
        return redirect(url_for("auth.login"))

    # =====================================================
    # CONSUMIR API
    # =====================================================

    headers = {
        "Authorization": f"Bearer {access_token}"
    }

    try:

        response = requests.get(
            f"{API_URL}/appointments/my",
            headers=headers,
            timeout=10
        )

    except requests.RequestException as e:

        print(
            f"Erro ao conectar com API de appointments: {e}"
        )

        return render_template(
            "profession/professional_calendar.html",
            appointments=[],
            professional_id=None,
            api_error="Não foi possível conectar à API."
        )

    # =====================================================
    # TOKEN INVÁLIDO
    # =====================================================

    if response.status_code in [401, 422]:

        session.clear()

        return redirect(
            url_for("auth.login")
        )

    # =====================================================
    # ERRO DA API
    # =====================================================

    if response.status_code != 200:

        print(
            "Erro API appointments:",
            response.status_code,
            response.text
        )

        return render_template(
            "profession/professional_calendar.html",
            appointments=[],
            professional_id=None,
            api_error="Não foi possível carregar as consultas."
        )

    # =====================================================
    # JSON
    # =====================================================

    try:

        data = response.json()

    except ValueError:

        return render_template(
            "profession/professional_calendar.html",
            appointments=[],
            professional_id=None,
            api_error="Resposta inválida da API."
        )

    # =====================================================
    # APPOINTMENTS
    # =====================================================

    appointments = data.get(
        "appointments",
        []
    )

    # =====================================================
    # BUSCAR PERFIL PROFISSIONAL
    # =====================================================

    professional_id = session.get(
        "professional_id"
    )

    # =====================================================
    # RENDER
    # =====================================================

    return render_template(
        "profession/professional_calendar.html",
        appointments=appointments,
        professional_id=professional_id,
        api_error=None
    )

@web_bp.route("/profession/appointments")
def professional_appointments():

    # =====================================================
    # VERIFICAR AUTENTICAÇÃO
    # =====================================================

    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    # =====================================================
    # VERIFICAR PERMISSÃO
    # =====================================================

    if session.get("role") != "professional":
        abort(403)

    # =====================================================
    # TOKEN JWT
    # =====================================================

    access_token = session.get("access_token")

    if not access_token:

        session.clear()

        return redirect(
            url_for("auth.login")
        )

    # =====================================================
    # HEADERS
    # =====================================================

    headers = {
        "Authorization": f"Bearer {access_token}"
    }

    # =====================================================
    # CONSUMIR API
    # =====================================================

    try:

        response = requests.get(
            f"{API_URL}/appointments/my",
            headers=headers,
            timeout=10
        )

    except requests.RequestException as e:

        print(
            f"Erro ao conectar com API de appointments: {e}"
        )

        return render_template(
            "profession/professional_appointments.html",
            appointments=[],
            professional_id=None,
            api_error="Não foi possível conectar à API."
        )

    # =====================================================
    # TOKEN INVÁLIDO
    # =====================================================

    if response.status_code in [401, 422]:

        session.clear()

        return redirect(
            url_for("auth.login")
        )

    # =====================================================
    # ERRO DA API
    # =====================================================

    if response.status_code != 200:

        print(
            "Erro API appointments:",
            response.status_code,
            response.text
        )

        return render_template(
            "profession/professional_appointments.html",
            appointments=[],
            professional_id=None,
            api_error="Não foi possível carregar as consultas."
        )

    # =====================================================
    # JSON
    # =====================================================

    try:

        data = response.json()

    except ValueError:

        return render_template(
            "profession/professional_appointments.html",
            appointments=[],
            professional_id=None,
            api_error="Resposta inválida da API."
        )

    # =====================================================
    # APPOINTMENTS
    # =====================================================

    appointments = data.get(
        "appointments",
        []
    )

    # =====================================================
    # PROFESSIONAL ID
    # =====================================================

    professional_id = session.get(
        "professional_id"
    )

    # =====================================================
    # RENDER
    # =====================================================

    return render_template(
        "profession/professional_appointments.html",
        appointments=appointments,
        professional_id=professional_id,
        api_error=None
    )

@web_bp.route(
    "/profession/appointments/<int:appointment_id>/accept",
    methods=["PUT"]
)
def professional_accept_appointment(appointment_id):

    # ============================================
    # AUTENTICAÇÃO
    # ============================================

    if "user_id" not in session:
        return jsonify({
            "success": False,
            "message": "Sessão expirada."
        }), 401

    # ============================================
    # PERMISSÃO
    # ============================================

    if session.get("role") != "professional":
        return jsonify({
            "success": False,
            "message": "Acesso negado."
        }), 403

    # ============================================
    # TOKEN
    # ============================================

    access_token = session.get("access_token")

    if not access_token:
        session.clear()

        return jsonify({
            "success": False,
            "message": "Sessão expirada."
        }), 401

    # ============================================
    # CONSUMIR API
    # ============================================

    headers = {
        "Authorization": f"Bearer {access_token}"
    }

    try:

        response = requests.put(
            f"{API_URL}/appointments/{appointment_id}/accept",
            headers=headers,
            timeout=10
        )

    except requests.RequestException as e:

        print(
            f"Erro ao conectar com API: {e}"
        )

        return jsonify({
            "success": False,
            "message": "Erro de conexão com a API."
        }), 500

    # ============================================
    # TOKEN INVÁLIDO
    # ============================================

    if response.status_code in [401, 422]:

        session.clear()

        return jsonify({
            "success": False,
            "message": "Sessão expirada."
        }), 401

    # ============================================
    # RETORNAR RESPOSTA DA API
    # ============================================

    try:

        data = response.json()

    except ValueError:

        return jsonify({
            "success": False,
            "message": "Resposta inválida da API."
        }), 500

    return jsonify(data), response.status_code

@web_bp.route(
    "/profession/appointments/<int:appointment_id>/cancel",
    methods=["PUT"]
)
def professional_cancel_appointment(appointment_id):

    # ============================================
    # AUTENTICAÇÃO
    # ============================================

    if "user_id" not in session:
        return jsonify({
            "success": False,
            "message": "Sessão expirada."
        }), 401

    # ============================================
    # PERMISSÃO
    # ============================================

    if session.get("role") != "professional":
        return jsonify({
            "success": False,
            "message": "Acesso negado."
        }), 403

    # ============================================
    # TOKEN
    # ============================================

    access_token = session.get("access_token")

    if not access_token:

        session.clear()

        return jsonify({
            "success": False,
            "message": "Sessão expirada."
        }), 401

    # ============================================
    # HEADERS
    # ============================================

    headers = {
        "Authorization": f"Bearer {access_token}"
    }

    # ============================================
    # CONSUMIR API
    # ============================================

    try:

        response = requests.put(
            f"{API_URL}/appointments/{appointment_id}/cancel",
            headers=headers,
            timeout=10
        )

    except requests.RequestException as e:

        print(
            f"Erro ao conectar com API: {e}"
        )

        return jsonify({
            "success": False,
            "message": "Erro de conexão com a API."
        }), 500

    # ============================================
    # TOKEN INVÁLIDO
    # ============================================

    if response.status_code in [401, 422]:

        session.clear()

        return jsonify({
            "success": False,
            "message": "Sessão expirada."
        }), 401

    # ============================================
    # JSON
    # ============================================

    try:

        data = response.json()

    except ValueError:

        return jsonify({
            "success": False,
            "message": "Resposta inválida da API."
        }), 500

    return jsonify(data), response.status_code

# ============================
# RECEITAS
# ============================



@web_bp.route("/profession/patients/data", methods=["GET"])
def professional_patients_data():

    if "user_id" not in session:
        return jsonify({
            "success": False,
            "message": "Não autenticado."
        }), 401

    if session.get("role") != "professional":
        return jsonify({
            "success": False,
            "message": "Acesso negado."
        }), 403

    access_token = session.get("access_token")

    if not access_token:
        session.clear()

        return jsonify({
            "success": False,
            "message": "Sessão expirada."
        }), 401

    headers = {
        "Authorization": f"Bearer {access_token}"
    }

    try:

        response = requests.get(
            f"{API_URL}/patient-professional/my-patients",
            headers=headers,
            timeout=10
        )

    except requests.RequestException as e:

        print(
            f"Erro ao conectar com API de patients: {e}"
        )

        return jsonify({
            "success": False,
            "message": "Não foi possível conectar à API."
        }), 500

    if response.status_code in [401, 422]:

        session.clear()

        return jsonify({
            "success": False,
            "message": "Sessão expirada."
        }), 401

    if response.status_code != 200:

        print(
            "Erro API patients:",
            response.status_code,
            response.text
        )

        return jsonify({
            "success": False,
            "message": "Não foi possível carregar os pacientes."
        }), response.status_code

    try:

        data = response.json()

    except ValueError:

        return jsonify({
            "success": False,
            "message": "Resposta inválida da API."
        }), 500

    # =====================================================
    # DEBUG - PACIENTES RECEBIDOS DA API
    # =====================================================

    print("========================================")
    print("PACIENTES RECEBIDOS DA API:")
    print(data)
    print("========================================")

    return jsonify(data), 200


@web_bp.route(
    "/profession/prescriptions",
    methods=["GET", "POST"]
)
def professional_prescriptions(
):

    # =====================================================
    # VERIFICAR AUTENTICAÇÃO
    # =====================================================

    if "user_id" not in session:

        if request.method == "POST":
            return jsonify({
                "success": False,
                "message": "Não autenticado."
            }), 401

        return redirect(
            url_for("auth.login")
        )

    # =====================================================
    # VERIFICAR PERMISSÃO
    # =====================================================

    if session.get("role") != "professional":

        if request.method == "POST":
            return jsonify({
                "success": False,
                "message": "Acesso negado."
            }), 403

        abort(403)

    # =====================================================
    # TOKEN JWT
    # =====================================================

    access_token = session.get(
        "access_token"
    )

    if not access_token:

        session.clear()

        if request.method == "POST":
            return jsonify({
                "success": False,
                "message": "Sessão expirada."
            }), 401

        return redirect(
            url_for("auth.login")
        )

    # =====================================================
    # HEADERS
    # =====================================================

    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }

    # =====================================================
    # POST — CRIAR RECEITA
    # =====================================================

    if request.method == "POST":

        data = request.get_json()

        if not data:

            return jsonify({
                "success": False,
                "message": "JSON body is required."
            }), 400

        print("========================================")
        print("CRIAR RECEITA")
        print("DADOS RECEBIDOS DO FRONTEND:")
        print(data)
        print("========================================")

        try:

            response = requests.post(
                f"{API_URL}/prescriptions/create",
                headers=headers,
                json=data,
                timeout=10
            )

        except requests.RequestException as e:

            print(
                f"Erro ao conectar com API de prescriptions: {e}"
            )

            return jsonify({
                "success": False,
                "message": "Não foi possível conectar à API."
            }), 500

        # =================================================
        # TOKEN INVÁLIDO
        # =================================================

        if response.status_code in [401, 422]:

            session.clear()

            return jsonify({
                "success": False,
                "message": "Sessão expirada."
            }), 401

        # =================================================
        # RESPOSTA DA API
        # =================================================

        try:

            result = response.json()

        except ValueError:

            print(
                "Resposta inválida da API:",
                response.text
            )

            return jsonify({
                "success": False,
                "message": "Resposta inválida da API."
            }), 500

        # =================================================
        # ERRO DA API
        # =================================================

        if response.status_code not in [200, 201]:

            print(
                "Erro API create prescription:",
                response.status_code,
                response.text
            )

            return jsonify(result), response.status_code

        # =================================================
        # SUCESSO
        # =================================================

        print("========================================")
        print("RECEITA CRIADA COM SUCESSO")
        print("RESPOSTA DA API:")
        print(result)
        print("========================================")

        return jsonify(result), response.status_code

    # =====================================================
    # GET — LISTAR RECEITAS
    # =====================================================

    try:

        response = requests.get(
            f"{API_URL}/prescriptions/my",
            headers=headers,
            timeout=10
        )

    except requests.RequestException as e:

        print(
            f"Erro ao conectar com API de prescriptions: {e}"
        )

        return render_template(
            "profession/professional_prescriptions.html",
            prescriptions=[],
            professional_id=None,
            api_error="Não foi possível conectar à API."
        )

    # =====================================================
    # TOKEN INVÁLIDO
    # =====================================================

    if response.status_code in [401, 422]:

        session.clear()

        return redirect(
            url_for("auth.login")
        )

    # =====================================================
    # ERRO DA API
    # =====================================================

    if response.status_code != 200:

        print(
            "Erro API prescriptions:",
            response.status_code,
            response.text
        )

        return render_template(
            "profession/professional_prescriptions.html",
            prescriptions=[],
            professional_id=None,
            api_error="Não foi possível carregar as receitas."
        )

    # =====================================================
    # JSON
    # =====================================================

    try:

        data = response.json()

    except ValueError:

        return render_template(
            "profession/professional_prescriptions.html",
            prescriptions=[],
            professional_id=None,
            api_error="Resposta inválida da API."
        )

    # =====================================================
    # PRESCRIPTIONS
    # =====================================================

    prescriptions = data.get(
        "prescriptions",
        []
    )

    # =====================================================
    # PROFESSIONAL ID
    # =====================================================

    professional_id = session.get(
        "professional_id"
    )

    # =====================================================
    # RENDER
    # =====================================================

    return render_template(
        "profession/professional_prescriptions.html",
        prescriptions=prescriptions,
        professional_id=professional_id,
        api_error=None
    )


@web_bp.route("/profession/prescriptions/data", methods=["GET"])
def professional_prescriptions_data():

    if "user_id" not in session:
        return jsonify({
            "success": False,
            "message": "Não autenticado."
        }), 401

    if session.get("role") != "professional":
        return jsonify({
            "success": False,
            "message": "Acesso negado."
        }), 403

    access_token = session.get("access_token")

    if not access_token:
        session.clear()

        return jsonify({
            "success": False,
            "message": "Sessão expirada."
        }), 401

    headers = {
        "Authorization": f"Bearer {access_token}"
    }

    try:

        response = requests.get(
            f"{API_URL}/prescriptions/my",
            headers=headers,
            timeout=10
        )

    except requests.RequestException as e:

        print(
            f"Erro ao conectar com API de prescriptions: {e}"
        )

        return jsonify({
            "success": False,
            "message": "Não foi possível conectar à API."
        }), 500

    if response.status_code in [401, 422]:

        session.clear()

        return jsonify({
            "success": False,
            "message": "Sessão expirada."
        }), 401

    if response.status_code != 200:

        print(
            "Erro API prescriptions:",
            response.status_code,
            response.text
        )

        return jsonify({
            "success": False,
            "message": "Não foi possível carregar as receitas."
        }), response.status_code

    try:

        data = response.json()

    except ValueError:

        return jsonify({
            "success": False,
            "message": "Resposta inválida da API."
        }), 500

    return jsonify(data), 200



# ============================
# EXAMES
# ============================

@web_bp.route("/profession/exams")
def professional_exams():

    if session.get("role") != "professional":
        abort(403)

    return render_template(
        "profession/professional_exams.html"
    )


# ============================
# MENSAGENS
# ============================

@web_bp.route("/profession/messages")
def professional_messages():

    # =====================================================
    # VERIFICAR PERMISSÃO
    # =====================================================

    if session.get("role") != "professional":
        abort(403)

    # =====================================================
    # VERIFICAR AUTENTICAÇÃO
    # =====================================================

    token = session.get("access_token")
    user_id = session.get("user_id")

    if not token or not user_id:

        flash(
            "Sessão expirada. Faça login novamente.",
            "warning"
        )

        return redirect(
            url_for("auth.login")
        )

    # =====================================================
    # HEADERS
    # =====================================================

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    # =====================================================
    # CONSUMIR API
    # =====================================================

    api_url = (
        f"{API_URL}/api/messages/{user_id}"
    )

    messages = []

    try:

        response = requests.get(
            api_url,
            headers=headers,
            timeout=10
        )

    except requests.RequestException as e:

        print(
            "ERRO AO BUSCAR MENSAGENS DO PROFISSIONAL:",
            repr(e),
            flush=True
        )

        flash(
            "Não foi possível conectar ao servidor.",
            "danger"
        )

        return render_template(
            "profession/professional_messages.html",
            messages=[]
        )

    # =====================================================
    # TOKEN EXPIRADO
    # =====================================================

    if response.status_code in [401, 422]:

        session.clear()

        flash(
            "Sua sessão expirou. Faça login novamente.",
            "warning"
        )

        return redirect(
            url_for("auth.login")
        )

    # =====================================================
    # PROCESSAR RESPOSTA
    # =====================================================

    try:

        result = response.json()

    except ValueError:

        print(
            "RESPOSTA INVÁLIDA DA API DE MENSAGENS:",
            response.text,
            flush=True
        )

        flash(
            "A API retornou uma resposta inválida.",
            "danger"
        )

        return render_template(
            "profession/professional_messages.html",
            messages=[]
        )

    # =====================================================
    # SUCESSO
    # =====================================================

    if response.status_code == 200 and result.get("success"):

        messages = result.get(
            "messages",
            []
        )

    else:

        flash(
            result.get(
                "message",
                "Não foi possível carregar as mensagens."
            ),
            "danger"
        )

    # =====================================================
    # TEMPLATE
    # =====================================================

    return render_template(
        "profession/professional_messages.html",
        messages=messages
    )




# ============================
# HISTÓRICO
# ============================

@web_bp.route("/profession/history")
def professional_history():

    if session.get("role") != "professional":
        abort(403)

    return render_template(
        "profession/professional_history.html"
    )


# ============================
# RELATÓRIOS
# ============================

@web_bp.route("/profession/reports")
def professional_reports():

    if session.get("role") != "professional":
        abort(403)

    return render_template(
        "profession/professional_reports.html"
    )


# ============================
# PERFIL PROFISSIONAL
# ============================

@web_bp.route(
    "/profession/profile",
    methods=["GET", "POST"]
)
def professional_profile():

    token = session.get("access_token")
    user_id = session.get("user_id") or session.get("id")


    # =====================================================
    # VERIFICAR SESSÃO
    # =====================================================

    if not token or not user_id:

        flash(
            "Sessão expirada. Faça login novamente.",
            "danger"
        )

        return redirect(
            url_for("auth.login")
        )


    # =====================================================
    # HEADERS
    # =====================================================

    headers = {
        "Authorization": f"Bearer {token}"
    }


    # =====================================================
    # PROCESSAMENTO DO SALVAMENTO (POST)
    # =====================================================

    if request.method == "POST":

        # -------------------------------------------------
        # DADOS DA TABELA USERS
        # -------------------------------------------------

        full_name = request.form.get(
            "full_name"
        )

        email = request.form.get(
            "email"
        )

        new_password = request.form.get(
            "new_password"
        )

        confirm_password = request.form.get(
            "confirm_password"
        )


        # -------------------------------------------------
        # DADOS DA TABELA PROFESSIONALS
        # -------------------------------------------------

        specialty = request.form.get(
            "specialty"
        )

        license_number = request.form.get(
            "license_number"
        )

        institution = request.form.get(
            "institution"
        )

        practice_area = request.form.get(
            "practice_area"
        )

        phone = request.form.get(
            "phone"
        )

        professional_email = request.form.get(
            "professional_email"
        )


        # =================================================
        # VALIDAR SENHA
        # =================================================

        if new_password:

            if new_password != confirm_password:

                flash(
                    "A confirmação da nova senha não coincide.",
                    "warning"
                )

                return redirect(
                    url_for("web.professional_profile")
                )


            password_to_send = new_password

        else:

            password_to_send = ""


        # =================================================
        # PAYLOAD
        # =================================================

        payload = {

            "full_name": full_name,

            "email": email,

            "password": password_to_send,

            "specialty": specialty,

            "license_number": license_number,

            "institution": institution,

            "practice_area": practice_area,

            "phone": phone,

            "professional_email":
                professional_email

        }


        # =================================================
        # FOTO DE PERFIL
        # =================================================

        files = {}


        if "profile_photo" in request.files:

            file = request.files[
                "profile_photo"
            ]


            if file and file.filename != "":

                files = {

                    "profile_photo": (

                        file.filename,

                        file.stream,

                        file.mimetype

                    )

                }

            else:

                payload["profile_photo"] = (
                    session.get(
                        "profile_photo",
                        ""
                    )
                )


        # =================================================
        # URL DA API
        # =================================================

        api_url_update = (
            f"{API_URL}/professional/profile"
        )


        try:

            # =================================================
            # ENVIAR PARA API
            # =================================================

            response = requests.put(

                api_url_update,

                data=payload,

                files=files if files else None,

                headers=headers,

                timeout=10

            )


            try:

                result = response.json()


                if (

                    response.status_code == 200

                    and result.get("success")

                ):

                    # -------------------------------------
                    # SINCRONIZAR SESSÃO
                    # -------------------------------------

                    session["user_name"] = (
                        full_name
                    )

                    session["user_email"] = (
                        email
                    )


                    # -------------------------------------
                    # FOTO
                    # -------------------------------------

                    if (

                        "professional" in result

                        and
                        "profile_photo"
                        in result["professional"]

                    ):

                        profile_photo = (
                            result["professional"][
                                "profile_photo"
                            ]
                        )


                        if profile_photo:

                            filename = (
                                str(profile_photo)
                                .replace("\\", "/")
                                .split("/")[-1]
                            )


                            current_hostname = (
                                request.host.split(":")[0]
                            )


                            session["profile_photo"] = (
                                f"http://"
                                f"{current_hostname}:5001/"
                                f"uploads/profile_photos/"
                                f"{filename}"
                            )


                    flash(
                        "Informações do perfil atualizadas "
                        "com sucesso!",
                        "success"
                    )


                else:

                    flash(

                        result.get(
                            "message",
                            "Erro ao atualizar perfil."
                        ),

                        "danger"

                    )


            except ValueError:

                flash(

                    "A API retornou uma resposta "
                    "inválida ao salvar.",

                    "danger"

                )


        except requests.RequestException:

            flash(

                "Erro de conexão ao salvar alterações.",

                "danger"

            )


        return redirect(
            url_for("web.professional_profile")
        )


    # =====================================================
    # CARREGAMENTO INICIAL DOS DADOS (GET)
    # =====================================================

    professional_data = {

        # ---------------- USERS ----------------

        "full_name":
            session.get(
                "user_name",
                ""
            ),

        "email":
            session.get(
                "user_email",
                ""
            ),

        "profile_photo":
            session.get(
                "profile_photo",
                ""
            ),

        "role":
            "Profissional",

        "profile_type":
            "professional",

        "active":
            1,

        "created_at":
            "--",

        "last_login":
            "Nunca",


        # ---------------- PROFESSIONALS ----------------

        "specialty":
            "",

        "license_number":
            "",

        "institution":
            "",

        "practice_area":
            "",

        "phone":
            "",

        "professional_email":
            ""

    }


    # =====================================================
    # BUSCAR DADOS NA API
    # =====================================================

    headers_get = {
        **headers,
        "Content-Type":
            "application/json"
    }


    api_url_details = (
        f"{API_URL}/professional/profile"
    )


    try:

        response = requests.get(

            api_url_details,

            headers=headers_get,

            timeout=10

        )


        if response.status_code == 200:

            try:

                res_json = response.json()


                if (

                    res_json.get("success")

                    and
                    res_json.get("professional")

                ):

                    professional_data = (
                        res_json.get(
                            "professional"
                        )
                    )


                    # -------------------------------------
                    # FOTO
                    # -------------------------------------

                    profile_photo = (
                        professional_data.get(
                            "profile_photo"
                        )
                    )


                    if profile_photo:

                        filename = (
                            str(profile_photo)
                            .replace("\\", "/")
                            .split("/")[-1]
                        )


                        current_hostname = (
                            request.host.split(":")[0]
                        )


                        profile_photo_url = (
                            f"http://"
                            f"{current_hostname}:5001/"
                            f"uploads/profile_photos/"
                            f"{filename}"
                        )


                        professional_data[
                            "profile_photo"
                        ] = profile_photo_url


                        session[
                            "profile_photo"
                        ] = profile_photo_url


                    else:

                        professional_data[
                            "profile_photo"
                        ] = session.get(
                            "profile_photo",
                            ""
                        )


                    # -------------------------------------
                    # NOME
                    # -------------------------------------

                    if professional_data.get(
                        "full_name"
                    ):

                        session[
                            "user_name"
                        ] = professional_data[
                            "full_name"
                        ]


                    # -------------------------------------
                    # EMAIL
                    # -------------------------------------

                    if professional_data.get(
                        "email"
                    ):

                        session[
                            "user_email"
                        ] = professional_data[
                            "email"
                        ]


            except ValueError:

                print(
                    "Resposta da API de detalhes "
                    "não continha um JSON válido."
                )


        else:

            print(
                "API de detalhes retornou "
                f"status HTTP {response.status_code}"
            )


    except requests.RequestException as e:

        print(
            "Erro de conexão ao buscar detalhes "
            "do perfil profissional:",
            e
        )


    # =====================================================
    # RENDER
    # =====================================================

    return render_template(

        "profession/professional_profile.html",

        professional_data=professional_data

    )




# ============================
# CONFIGURAÇÕES
# ============================

@web_bp.route("/profession/settings")
def professional_settings():

    if session.get("role") != "professional":
        abort(403)

    return render_template(
        "profession/professional_settings.html"
    )

@web_bp.route("/patient/medical_record")
def medical_record():

    return render_template(
        "patient/medical_record.html"
    )

@web_bp.route("/patient/recipes")
def recipes():

    return render_template(
        "patient/recipes.html"
    )




@web_bp.route("/profession/clinical-records", methods=["GET", "POST"])
def professional_clinical_records():
    if session.get("role") != "professional":
        abort(403)

    token = session.get("access_token")
    user_id = session.get("user_id")

    if not token or not user_id:
        session.clear()
        flash("Sua sessão expirou. Faça login novamente.", "warning")
        return redirect(url_for("auth.login"))

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    api_url = f"{API_URL}/clinical-records"

    if request.method == "POST":
        data = {
            "appointment_id": request.form.get("appointment_id"),
            "diagnosis": request.form.get("diagnosis"),
            "treatment": request.form.get("treatment"),
            "prescription": request.form.get("prescription"),
            "notes": request.form.get("notes")
        }

        try:
            response = requests.post(
                f"{api_url}/create",
                headers=headers,
                json=data,
                timeout=10
            )

            result = response.json()

            if response.status_code == 201 and result.get("success"):
                flash("Prontuário criado com sucesso.", "success")
            else:
                flash(
                    result.get("message", "Não foi possível criar o prontuário."),
                    "danger"
                )

        except requests.RequestException:
            flash("Não foi possível conectar à API.", "danger")

        return redirect(url_for("web.professional_clinical_records"))

    return render_template("profession/clinical_records.html")

@web_bp.route("/patient/messages")
def messages():
    # 1. Verificar Autenticação
    if session.get("role") != "patient":
        abort(403)

    token = session.get("access_token")
    user_id = session.get("user_id")

    if not token or not user_id:
        session.clear()
        flash("Sessão expirada ou inválida. Faça login novamente.", "warning")
        return redirect(url_for("auth.login"))

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    api_url = f"{API_URL}/messages/{user_id}"  # Certifique-se que API_URL está definida
    messages_list = []

    # 2. Buscar Mensagens da API
    try:
        response = requests.get(api_url, headers=headers, timeout=10)
    except requests.RequestException as e:
        print("ERRO AO BUSCAR MENSAGENS:", repr(e), flush=True)
        flash("Não foi possível conectar ao servidor de mensagens.", "danger")
        return render_template("patient/messages.html", messages=[], conversations={}, total_messages=0,
                               unread_messages=0, current_user_id=user_id)

    if response.status_code in [401, 422]:
        session.clear()
        flash("Sua sessão expirou. Faça login novamente.", "warning")
        return redirect(url_for("auth.login"))

    # 3. Processar Resposta
    try:
        result = response.json()
    except ValueError:
        flash("A API retornou uma resposta inválida.", "danger")
        return render_template("patient/messages.html", messages=[], conversations={}, total_messages=0,
                               unread_messages=0, current_user_id=user_id)

    if response.status_code == 200 and result.get("success"):
        messages_list = result.get("messages", [])
    else:
        flash(result.get("message", "Erro ao carregar mensagens."), "danger")

    # 4. Pré-processamento: Agrupar conversas e contar não lidas (Muito mais seguro que fazer no Jinja)
    conversations = {}
    total_unread = 0

    for msg in messages_list:
        sender_id = str(msg.get("sender_id"))

        if sender_id not in conversations:
            conversations[sender_id] = {
                "sender_id": sender_id,
                "sender_name": msg.get("sender_name", "Desconhecido"),
                "last_message": msg.get("message", ""),
                "sent_at": msg.get("sent_at", ""),
                "unread_count": 0
            }

        # Considera False, 0 ou None como não lida
        if not msg.get("is_read"):
            conversations[sender_id]["unread_count"] += 1
            total_unread += 1

    # 5. Renderizar Template
    return render_template(
        "patient/messages.html",
        messages=messages_list,
        conversations=conversations,
        total_messages=len(messages_list),
        unread_messages=total_unread,
        current_user_id=user_id
    )

@web_bp.route("/patient/prescriptions")
def prescriptions():

    return render_template(
        "patient/prescriptions.html"
    )


@web_bp.route("/invitation", methods=["GET", "POST"])
def invitation():

    # =====================================================
    # ABRIR PÁGINA
    # =====================================================

    if request.method == "GET":

        return render_template(
            "invitation.html"
        )


    # =====================================================
    # RECEBER DADOS DO FORMULÁRIO
    # =====================================================

    data = {

        "full_name": request.form.get("full_name"),

        "email": request.form.get("email"),

        "phone": request.form.get("phone"),

        "birth_date": request.form.get("birth_date"),

        "profile_type": request.form.get("profile_type"),

        "interest": request.form.get("interest")

    }


    # =====================================================
    # INICIAR VERIFICAÇÃO DO E-MAIL
    # =====================================================

    try:

        verification_response = requests.post(

            f"{API_URL}/api/verification/start",

            json={

                "email": data["email"],

                "phone": data["phone"]

            },

            timeout=10

        )

    except requests.RequestException:

        flash(
            "Não foi possível conectar ao servidor de verificação.",
            "danger"
        )

        return redirect(
            url_for("web.invitation")
        )


    # =====================================================
    # VERIFICAR RESPOSTA DA API
    # =====================================================

    try:

        verification_data = verification_response.json()

    except ValueError:

        flash(
            "Resposta inválida do servidor de verificação.",
            "danger"
        )

        return redirect(
            url_for("web.invitation")
        )


    if verification_response.status_code != 200:

        flash(

            verification_data.get(
                "message",
                "Não foi possível enviar o código de verificação."
            ),

            "danger"

        )

        return redirect(
            url_for("web.invitation")
        )


    # =====================================================
    # GUARDAR DADOS TEMPORARIAMENTE NA SESSION
    # =====================================================

    session["invitation_data"] = data

    session["verification_id"] = (
        verification_data["verification_id"]
    )


    # =====================================================
    # ABRIR MODAL DE VERIFICAÇÃO
    # =====================================================

    return render_template(

        "invitation.html",

        show_verification_modal=True,

        verification_id=verification_data["verification_id"]

    )



# =====================================================
# AGENDAMENTOS — PACIENTE
# API: POST /appointments/create
# =====================================================

@web_bp.route("/patient/appointments", methods=["GET", "POST"])
def patient_appointments():

    if request.method == "GET":
        return render_template("patient/appointments.html")

    if "user_id" not in session:
        flash("Faça login para continuar.", "warning")
        return redirect(url_for("auth.login"))

    if session.get("role") != "patient":
        flash("Acesso negado.", "danger")
        return redirect(url_for("web.index"))

    data = {
        "professional_id": request.form.get("professional_id"),
        "appointment_date": request.form.get("appointment_date"),
        "appointment_reason": request.form.get("appointment_reason"),
        "notes": request.form.get("notes")
    }

    try:
        response = requests.post(
            f"{API_URL}/appointments/create",
            json=data,
            headers={
                "Authorization": f"Bearer {session.get('access_token')}"
            },
            timeout=10
        )
        result = response.json()

    except (requests.RequestException, ValueError) as e:
        print("ERRO AO CRIAR AGENDAMENTO:", e)
        flash("Não foi possível conectar à API.", "danger")
        return redirect(url_for("web.patient_appointments"))

    if response.status_code == 201 and result.get("success"):
        flash(result.get("message", "Agendamento solicitado com sucesso!"), "success")
    else:
        flash(result.get("message", "Não foi possível criar o agendamento."), "danger")

    return redirect(url_for("web.appointments"))


# =====================================================
# AGENDAMENTOS — PROFISSIONAL
# API: POST /appointments/professional/create
# =====================================================

@web_bp.route("/profession/appointments", methods=["GET", "POST"])
def create_appointment():

    if request.method == "GET":
        return render_template("profession/professional_appointments.html")

    if "user_id" not in session:
        flash("Faça login para continuar.", "warning")
        return redirect(url_for("auth.login"))

    if session.get("role") != "professional":
        flash("Acesso negado.", "danger")
        return redirect(url_for("web.index"))

    data = {
        "patient_id": request.form.get("patient_id"),
        "appointment_date": request.form.get("appointment_date"),
        "appointment_reason": request.form.get("appointment_reason"),
        "notes": request.form.get("notes")
    }

    try:
        response = requests.post(
            f"{API_URL}/appointments/professional/create",
            json=data,
            headers={
                "Authorization": f"Bearer {session.get('access_token')}"
            },
            timeout=10
        )
        result = response.json()

    except (requests.RequestException, ValueError) as e:
        print("ERRO AO CRIAR AGENDAMENTO:", e)
        flash("Não foi possível conectar à API.", "danger")
        return redirect(url_for("web.create_appointment"))

    if response.status_code == 201 and result.get("success"):
        flash(result.get("message", "Agendamento criado com sucesso!"), "success")
    else:
        flash(result.get("message", "Não foi possível criar o agendamento."), "danger")

    return redirect(url_for("web.appointments"))


# =====================================================
# MEUS AGENDAMENTOS
# API: GET /appointments/my
# =====================================================

@web_bp.route("/appointments", methods=["GET"])
def appointments():

    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    role = session.get("role")

    if role == "patient":
        template = "patient/appointments.html"
    elif role == "professional":
        template = "profession/professional_appointments.html"
    elif role == "administrator":
        template = "admin/appointments.html"
    else:
        flash("Perfil inválido.", "danger")
        return redirect(url_for("auth.login"))

    try:
        response = requests.get(
            f"{API_URL}/appointments/my",
            headers={
                "Authorization": f"Bearer {session.get('access_token')}"
            },
            timeout=10
        )
        result = response.json()

    except (requests.RequestException, ValueError) as e:
        print("ERRO AO BUSCAR AGENDAMENTOS:", e)
        flash("Não foi possível carregar os agendamentos.", "danger")
        return render_template(template, appointments=[])

    if response.status_code != 200:
        flash(result.get("message", "Erro ao carregar agendamentos."), "danger")
        return render_template(template, appointments=[])

    if isinstance(result, list):
        appointments_data = result
    else:
        appointments_data = result.get("appointments", [])

    return render_template(
        template,
        appointments=appointments_data
    )


# =====================================================
# REAGENDAR
# API: PUT /appointments/<id>/reschedule
# =====================================================

@web_bp.route(
    "/profession/appointments/<int:appointment_id>/reschedule",
    methods=["POST"]
)
def reschedule_appointment(appointment_id):

    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    if session.get("role") != "professional":
        flash("Acesso negado.", "danger")
        return redirect(url_for("web.index"))

    data = {
        "appointment_date": request.form.get("appointment_date"),
        "reason": request.form.get("reason")
    }

    try:
        response = requests.put(
            f"{API_URL}/appointments/{appointment_id}/reschedule",
            json=data,
            headers={
                "Authorization": f"Bearer {session.get('access_token')}"
            },
            timeout=10
        )
        result = response.json()

    except (requests.RequestException, ValueError) as e:
        print("ERRO AO REAGENDAR:", e)
        flash("Não foi possível conectar à API.", "danger")
        return redirect(url_for("web.appointments"))

    if response.ok and result.get("success"):
        flash(result.get("message", "Agendamento reagendado!"), "success")
    else:
        flash(result.get("message", "Não foi possível reagendar."), "danger")

    return redirect(url_for("web.appointments"))


# =====================================================
# ACEITAR AGENDAMENTO
# API: PUT /appointments/<id>/accept
# =====================================================

@web_bp.route(
    "/profession/appointments/<int:appointment_id>/accept",
    methods=["POST"]
)
def accept_appointment(appointment_id):

    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    if session.get("role") != "professional":
        flash("Acesso negado.", "danger")
        return redirect(url_for("web.index"))

    try:
        response = requests.put(
            f"{API_URL}/appointments/{appointment_id}/accept",
            headers={
                "Authorization": f"Bearer {session.get('access_token')}"
            },
            timeout=10
        )
        result = response.json()

    except (requests.RequestException, ValueError) as e:
        print("ERRO AO ACEITAR AGENDAMENTO:", e)
        flash("Não foi possível conectar à API.", "danger")
        return redirect(url_for("web.appointments"))

    if response.ok and result.get("success"):
        flash(result.get("message", "Agendamento aceito!"), "success")
    else:
        flash(result.get("message", "Não foi possível aceitar o agendamento."), "danger")

    return redirect(url_for("web.appointments"))


# =====================================================
# CANCELAR AGENDAMENTO
# API: PUT /appointments/<id>/cancel
# =====================================================

@web_bp.route(
    "/appointments/<int:appointment_id>/cancel",
    methods=["POST"]
)
def cancel_appointment(appointment_id):

    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    try:
        response = requests.put(
            f"{API_URL}/appointments/{appointment_id}/cancel",
            headers={
                "Authorization": f"Bearer {session.get('access_token')}"
            },
            timeout=10
        )
        result = response.json()

    except (requests.RequestException, ValueError) as e:
        print("ERRO AO CANCELAR AGENDAMENTO:", e)
        flash("Não foi possível conectar à API.", "danger")
        return redirect(url_for("web.appointments"))

    if response.ok and result.get("success"):
        flash(result.get("message", "Agendamento cancelado!"), "success")
    else:
        flash(result.get("message", "Não foi possível cancelar o agendamento."), "danger")

    return redirect(url_for("web.appointments"))


# =====================================================
# ADMINISTRADOR — TODOS OS AGENDAMENTOS
# API: GET /appointments/all
# =====================================================

@web_bp.route("/admin/appointments", methods=["GET"])
def all_appointments():

    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    if session.get("role") != "administrator":
        flash("Acesso negado.", "danger")
        return redirect(url_for("web.index"))

    try:
        response = requests.get(
            f"{API_URL}/appointments/all",
            headers={
                "Authorization": f"Bearer {session.get('access_token')}"
            },
            timeout=10
        )
        result = response.json()

    except (requests.RequestException, ValueError) as e:
        print("ERRO AO BUSCAR AGENDAMENTOS:", e)
        flash("Não foi possível carregar os agendamentos.", "danger")
        return render_template(
            "admin/appointments.html",
            appointments=[]
        )

    if response.status_code != 200:
        flash(result.get("message", "Erro ao carregar agendamentos."), "danger")
        return render_template(
            "admin/appointments.html",
            appointments=[]
        )

    return render_template(
        "admin/appointments.html",
        appointments=result.get("appointments", [])
    )


@web_bp.route("/verification/email", methods=["POST"])
def verification_email():

    print("", flush=True)
    print("====================================================", flush=True)
    print("WEB - VERIFICAÇÃO DE E-MAIL", flush=True)
    print("====================================================", flush=True)


    # =====================================================
    # RECEBER JSON DO NAVEGADOR
    # =====================================================

    data = request.get_json(silent=True)

    print(
        "JSON RECEBIDO:",
        data,
        flush=True
    )


    # =====================================================
    # VALIDAR JSON
    # =====================================================

    if not data:

        print(
            "ERRO: JSON NÃO RECEBIDO.",
            flush=True
        )

        return jsonify({

            "success": False,

            "message": "Dados de verificação não enviados."

        }), 400


    # =====================================================
    # PEGAR DADOS
    # =====================================================

    verification_id = data.get(
        "verification_id"
    )

    code = data.get(
        "code"
    )


    print(
        "VERIFICATION ID:",
        repr(verification_id),
        flush=True
    )

    print(
        "CODE:",
        repr(code),
        flush=True
    )


    # =====================================================
    # VALIDAR VERIFICATION ID
    # =====================================================

    if not verification_id:

        print(
            "ERRO: verification_id AUSENTE.",
            flush=True
        )

        return jsonify({

            "success": False,

            "message": "ID da verificação é obrigatório."

        }), 400


    # =====================================================
    # VALIDAR CÓDIGO
    # =====================================================

    if not code:

        print(
            "ERRO: code AUSENTE.",
            flush=True
        )

        return jsonify({

            "success": False,

            "message": "Código de verificação é obrigatório."

        }), 400


    # =====================================================
    # ENVIAR PARA API DE VERIFICAÇÃO
    # =====================================================

    print(
        "ENVIANDO PARA API...",
        flush=True
    )

    print(
        "URL:",
        f"{API_URL}/api/verification/email",
        flush=True
    )


    try:

        response = requests.post(

            f"{API_URL}/api/verification/email",

            json={

                "verification_id":
                    verification_id,

                "code":
                    code

            },

            timeout=10

        )


    except requests.RequestException as e:

        print(
            "ERRO AO CONECTAR COM API:",
            repr(e),
            flush=True
        )

        return jsonify({

            "success": False,

            "message":
                "Não foi possível conectar ao servidor de verificação."

        }), 500


    # =====================================================
    # RESPOSTA DA API DE VERIFICAÇÃO
    # =====================================================

    print(
        "STATUS DA API:",
        response.status_code,
        flush=True
    )

    print(
        "RESPOSTA DA API:",
        response.text,
        flush=True
    )


    # =====================================================
    # CONVERTER RESPOSTA PARA JSON
    # =====================================================

    try:

        result = response.json()


    except ValueError:

        print(
            "ERRO: API NÃO RETORNOU JSON.",
            flush=True
        )

        return jsonify({

            "success": False,

            "message":
                "A API retornou uma resposta inválida."

        }), 500


    # =====================================================
    # SE O CÓDIGO FOR INVÁLIDO / EXPIRADO
    #
    # NÃO CRIA A SOLICITAÇÃO.
    # =====================================================

    if not result.get("success"):

        print(
            "VERIFICAÇÃO NÃO FOI CONCLUÍDA.",
            flush=True
        )

        print(
            "MENSAGEM:",
            result.get("message"),
            flush=True
        )

        print(
            "====================================================",
            flush=True
        )

        return jsonify(
            result
        ), response.status_code


    # =====================================================
    # E-MAIL CONFIRMADO
    # =====================================================

    print(
        "====================================================",
        flush=True
    )

    print(
        "E-MAIL VERIFICADO COM SUCESSO.",
        flush=True
    )

    print(
        "Agora vamos criar a solicitação de convite.",
        flush=True
    )


    # =====================================================
    # RECUPERAR DADOS DA SOLICITAÇÃO
    # =====================================================
    #
    # Esses dados foram salvos anteriormente em:
    #
    # session["invitation_data"]
    #
    # dentro da rota /invitation.
    #
    # =====================================================

    invitation_data = session.get(
        "invitation_data"
    )


    print(
        "DADOS DA SOLICITAÇÃO NA SESSION:",
        invitation_data,
        flush=True
    )


    # =====================================================
    # VERIFICAR SE OS DADOS EXISTEM
    # =====================================================

    if not invitation_data:

        print(
            "ERRO: invitation_data NÃO ENCONTRADO NA SESSION.",
            flush=True
        )

        return jsonify({

            "success": False,

            "message":
                "Os dados da solicitação não foram encontrados. Recarregue a página e tente novamente."

        }), 400


    # =====================================================
    # CRIAR SOLICITAÇÃO NA TABELA invitations
    # =====================================================

    print(
        "ENVIANDO DADOS PARA CRIAÇÃO DA SOLICITAÇÃO...",
        flush=True
    )

    print(
        "URL:",
        f"{API_URL}/api/invitation",
        flush=True
    )


    try:

        invitation_response = requests.post(

            f"{API_URL}/api/invitation",

            json={

                "full_name":
                    invitation_data.get(
                        "full_name"
                    ),

                "email":
                    invitation_data.get(
                        "email"
                    ),

                "phone":
                    invitation_data.get(
                        "phone"
                    ),

                "birth_date":
                    invitation_data.get(
                        "birth_date"
                    ),

                "profile_type":
                    invitation_data.get(
                        "profile_type"
                    ),

                "interest":
                    invitation_data.get(
                        "interest"
                    )

            },

            timeout=10

        )


    except requests.RequestException as e:

        print(
            "ERRO AO CRIAR SOLICITAÇÃO:",
            repr(e),
            flush=True
        )

        return jsonify({

            "success": False,

            "message":
                "O e-mail foi verificado, mas não foi possível criar a solicitação de convite."

        }), 500


    # =====================================================
    # RESPOSTA DA API DE CONVITE
    # =====================================================

    print(
        "STATUS DA API DE CONVITE:",
        invitation_response.status_code,
        flush=True
    )

    print(
        "RESPOSTA DA API DE CONVITE:",
        invitation_response.text,
        flush=True
    )


    # =====================================================
    # CONVERTER RESPOSTA
    # =====================================================

    try:

        invitation_result = (
            invitation_response.json()
        )


    except ValueError:

        print(
            "ERRO: API DE CONVITE NÃO RETORNOU JSON.",
            flush=True
        )

        return jsonify({

            "success": False,

            "message":
                "A API de convite retornou uma resposta inválida."

        }), 500


    # =====================================================
    # VERIFICAR SE A SOLICITAÇÃO FOI CRIADA
    # =====================================================

    if not invitation_result.get(
        "success"
    ):

        print(
            "ERRO AO SALVAR SOLICITAÇÃO.",
            flush=True
        )

        print(
            "MENSAGEM:",
            invitation_result.get(
                "message"
            ),
            flush=True
        )

        return jsonify({

            "success": False,

            "message":
                invitation_result.get(

                    "message",

                    "E-mail verificado, mas não foi possível criar a solicitação."

                )

        }), invitation_response.status_code


    # =====================================================
    # SOLICITAÇÃO CRIADA COM SUCESSO
    # =====================================================

    print(
        "====================================================",
        flush=True
    )

    print(
        "SOLICITAÇÃO CRIADA COM SUCESSO.",
        flush=True
    )

    print(
        "INVITATION ID:",
        invitation_result.get(
            "invitation_id"
        ),
        flush=True
    )


    # =====================================================
    # LIMPAR DADOS TEMPORÁRIOS DA SESSION
    # =====================================================

    session.pop(
        "invitation_data",
        None
    )

    session.pop(
        "verification_id",
        None
    )


    # =====================================================
    # RESPOSTA FINAL PARA O JAVASCRIPT
    # =====================================================

    print(
        "FLUXO COMPLETO FINALIZADO.",
        flush=True
    )

    print(
        "====================================================",
        flush=True
    )


    return jsonify({

        "success": True,

        "message":
            "E-mail verificado e solicitação de convite criada com sucesso.",

        "verification_id":
            verification_id,

        "invitation_id":
            invitation_result.get(
                "invitation_id"
            )

    }), 200




@web_bp.route("/patient/profile")
def patient_profile():

    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    response = requests.get(
        f"{API_URL}/api/patient/profile/{session['user_id']}"
    )

    print("STATUS:", response.status_code)
    print("CONTENT TYPE:", response.headers.get("Content-Type"))
    print("RESPOSTA API:", response.text)

    result = response.json()

    return render_template(
        "patient/profile.html",
        profile=result["profile"]
    )

@web_bp.route('/user_registration')
def user_registration():
    return render_template(
        'user_registration.html'
    )

@web_bp.route("/patient/dashboard")
def patient_dashboard():

    # verifica login
    if "user_id" not in session:
        return redirect(
            url_for("auth.login")
        )


    user_id = session["user_id"]


    # chama API do paciente
    response = requests.get(
        f"{API_URL}/api/patient/dashboard/{user_id}"
    )


    if response.status_code != 200:

        flash(
            "Erro ao carregar dashboard.",
            "danger"
        )

        return redirect(
            url_for("web.home")
        )


    data = response.json()


    return render_template(
        "patient/dashboard.html",

        user=data["user"],

        current_date=data["current_date"],

        next_appointment=data["next_appointment"],

        pending_exams=data["pending_exams"],

        unread_messages=data["unread_messages"],

        unread_notifications=data["unread_notifications"],

        recent_appointments=data["recent_appointments"],

        upcoming_appointments=data["upcoming_appointments"],

        timeline=data["timeline"],

        health_summary=data["health_summary"],

        medical_documents=data["medical_documents"],

        notifications=data["notifications"]
    )



