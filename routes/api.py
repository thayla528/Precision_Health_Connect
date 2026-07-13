from flask import Blueprint, request, jsonify
from database.bank import conectar

api_bp = Blueprint("api", __name__)


# ---------------- CRIAR CONVITE ----------------
@api_bp.route("/api/convites", methods=["POST"])
def criar_convite():

    dados = request.get_json()

    nome = dados.get("nome_completo")
    email = dados.get("email")
    telefone = dados.get("telefone")
    data_nascimento = dados.get("data_nascimento")
    tipo_perfil = dados.get("tipo_perfil")
    motivo = dados.get("motivo_interesse")

    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO convites (
            nome_completo,
            email,
            telefone,
            data_nascimento,
            tipo_perfil,
            motivo_interesse
        )
        VALUES (?, ?, ?, ?, ?, ?)
    """, (
        nome,
        email,
        telefone,
        data_nascimento,
        tipo_perfil,
        motivo
    ))

    conn.commit()
    conn.close()

    return jsonify({
        "mensagem": "Solicitação enviada com sucesso."
    }), 201