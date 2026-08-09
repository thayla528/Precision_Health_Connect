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


# =====================================================
# RECUPERAÇÃO DE SENHA
# WEB -> API
# =====================================================

# =====================================================
# RECUPERAÇÃO DE SENHA
# WEB -> API
# =====================================================

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

@web_bp.route("/admin/profile")
def profiles():

    if session.get("role") != "administrator":
        abort(403)

    user_id = session.get("user_id")

    if not user_id:
        abort(401)

    try:

        response = requests.get(
            f"{API_URL}/api/admin/profile",
            params={
                "user_id": user_id
            }
        )

        data = response.json()

        if not response.ok or not data.get("success"):

            flash(
                "Não foi possível carregar o perfil.",
                "danger"
            )

            return render_template(
                "admin/profile.html",
                user=None,
                administrator=None
            )

        return render_template(
            "admin/profile.html",
            user=data.get("user"),
            administrator=data.get("administrator")
        )

    except Exception as e:

        print(
            "ERRO AO BUSCAR PERFIL DO ADMINISTRADOR:",
            e,
            flush=True
        )

        flash(
            "Erro ao conectar com a API.",
            "danger"
        )

        return render_template(
            "admin/profile.html",
            user=None,
            administrator=None
        )

@web_bp.route("/admin/users")
def users():

    return render_template(
        "admin/users.html"
    )

@web_bp.route("/admin/admin")
def admin():

    return render_template(
        "admin/admin.html"
    )

@web_bp.route("/admin/recent_logins")
def recent_logins():

    return render_template(
        "admin/recent_logins.html"
    )

@web_bp.route("/professional")
def health_professional_zone():

    if session.get("role") != "professional":
        abort(403)

    return redirect(
        url_for("web.health_professional_dashboard")
    )

@web_bp.route("/admin/logs")
def logs():

    return render_template(
        "admin/logs.html"
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


# ============================
# PACIENTES
# ============================

@web_bp.route("/profession/patients")
def professional_patients():

    if session.get("role") != "professional":
        abort(403)

    return render_template(
        "profession/professional_patients.html"
    )


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


# ============================
# AGENDA MÉDICA
# ============================

@web_bp.route("/profession/calendar")
def professional_calendar():

    if session.get("role") != "professional":
        abort(403)

    return render_template(
        "profession/professional_calendar.html"
    )


# ============================
# CONSULTAS
# ============================

@web_bp.route("/profession/appointments")
def professional_appointments():

    if session.get("role") != "professional":
        abort(403)

    return render_template(
        "profession/professional_appointments.html"
    )


# ============================
# RECEITAS
# ============================

@web_bp.route("/profession/prescriptions")
def professional_prescriptions():

    if session.get("role") != "professional":
        abort(403)

    return render_template(
        "profession/professional_prescriptions.html"
    )


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

    if session.get("role") != "professional":
        abort(403)

    return render_template(
        "profession/professional_messages.html"
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

@web_bp.route("/profession/profile")
def professional_profile():

    if session.get("role") != "professional":
        abort(403)

    return render_template(
        "profession/professional_profile.html"
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

@web_bp.route("/patient/messages")
def messages():

    return render_template(
        "patient/messages.html"
    )

@web_bp.route("/patient/prescriptions")
def prescriptions():

    return render_template(
        "patient/prescriptions.html"
    )

@web_bp.route("/appointments")
def appointments():
    return  render_template("patient/appointments.html")




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



