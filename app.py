
import os
import sys

from flask import Flask, request
from flask_wtf.csrf import CSRFProtect

from routes.web import web_bp, web_password_forgot, web_password_reset
from routes.auth import auth_bp


# =====================================================
# CRIAR APLICAÇÃO
# =====================================================

print()
print("1️⃣ INICIANDO APP", flush=True)

app = Flask(__name__)

print("2️⃣ APP CRIADO", flush=True)


# =====================================================
# SECRET KEY
# =====================================================

app.secret_key = os.getenv(
    "SECRET_KEY",
    "dev-key-segura"
)

print("3️⃣ SECRET KEY CONFIGURADA", flush=True)


# =====================================================
# CSRF
# =====================================================

print("4️⃣ CRIANDO CSRF", flush=True)

csrf = CSRFProtect()

print("5️⃣ CSRF CRIADO", flush=True)


print("6️⃣ INICIANDO CSRF NO APP", flush=True)

csrf.init_app(app)

print("7️⃣ CSRF INICIALIZADO", flush=True)


# =====================================================
# EXCEÇÃO CSRF PARA AUTH
# =====================================================

print(
    "8️⃣ APLICANDO CSRF EXEMPT NO AUTH",
    flush=True
)

csrf.exempt(web_password_forgot)
csrf.exempt(web_password_reset)


print(
    "9️⃣ AUTH EXEMPT APLICADO",
    flush=True
)


# =====================================================
# REGISTRAR WEB BLUEPRINT
# =====================================================

print(
    "🔟 REGISTRANDO WEB BLUEPRINT",
    flush=True
)

app.register_blueprint(web_bp)

print()
print("====================================================")
print("VERIFICANDO ROTAS DE PASSWORD RESET")
print("====================================================")

for rule in app.url_map.iter_rules():

    if "password" in str(rule):

        print(
            rule,
            "->",
            rule.endpoint,
            "->",
            rule.methods,
            flush=True
        )

print("====================================================")
print()

print(
    "1️⃣1️⃣ WEB BLUEPRINT REGISTRADO",
    flush=True
)


# =====================================================
# REGISTRAR AUTH BLUEPRINT
# =====================================================

print(
    "1️⃣2️⃣ REGISTRANDO AUTH BLUEPRINT",
    flush=True
)

app.register_blueprint(auth_bp)

print(
    "1️⃣3️⃣ AUTH BLUEPRINT REGISTRADO",
    flush=True
)


# =====================================================
# DEBUG - ROTAS REGISTRADAS
# =====================================================

print()
print("====================================================")
print("1️⃣4️⃣ ROTAS REGISTRADAS NO FLASK")
print("====================================================")

for rule in app.url_map.iter_rules():

    print(
        rule,
        "->",
        rule.endpoint,
        "->",
        rule.methods,
        flush=True
    )

print("====================================================")
print("1️⃣4️⃣ FIM DAS ROTAS")
print("====================================================")
print()


# =====================================================
# DEBUG GLOBAL DE TODAS AS REQUISIÇÕES
# =====================================================

@app.before_request
def debug_global_request():

    print()
    print("############################################")
    print("REQUISIÇÃO GLOBAL")
    print("############################################")

    print(
        "MÉTODO:",
        request.method,
        flush=True
    )

    print(
        "CAMINHO:",
        request.path,
        flush=True
    )

    print(
        "CONTENT TYPE:",
        request.content_type,
        flush=True
    )

    print(
        "CONTENT LENGTH:",
        request.content_length,
        flush=True
    )

    print(
        "JSON:",
        request.get_json(silent=True),
        flush=True
    )

    print(
        "FORM:",
        request.form,
        flush=True
    )

    print("############################################")
    print()


# =====================================================
# DEBUG - ERRO 400
# =====================================================

@app.errorhandler(400)
def handle_bad_request(error):

    print()
    print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
    print("ERRO 400 GLOBAL")
    print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")

    print(
        "CAMINHO:",
        request.path,
        flush=True
    )

    print(
        "MÉTODO:",
        request.method,
        flush=True
    )

    print(
        "CONTENT TYPE:",
        request.content_type,
        flush=True
    )

    print(
        "CONTENT LENGTH:",
        request.content_length,
        flush=True
    )

    print(
        "JSON:",
        request.get_json(silent=True),
        flush=True
    )

    print(
        "FORM:",
        request.form,
        flush=True
    )

    print(
        "ERRO:",
        error,
        flush=True
    )

    print(
        "DESCRIÇÃO:",
        getattr(
            error,
            "description",
            None
        ),
        flush=True
    )

    print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
    print()

    return {
        "success": False,
        "message": "Erro 400 capturado pela aplicação Web.",
        "error": str(error),
        "description": getattr(
            error,
            "description",
            None
        )
    }, 400


# =====================================================
# DEBUG - ERRO 403
# =====================================================

@app.errorhandler(403)
def handle_forbidden(error):

    print()
    print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
    print("ERRO 403")
    print("CAMINHO:", request.path, flush=True)
    print("MÉTODO:", request.method, flush=True)
    print("ERRO:", error, flush=True)
    print(
        "DESCRIÇÃO:",
        getattr(
            error,
            "description",
            None
        ),
        flush=True
    )
    print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
    print()

    return {
        "success": False,
        "message": "Acesso não autorizado.",
        "error": str(error)
    }, 403


# =====================================================
# DEBUG - ERRO 404
# =====================================================

@app.errorhandler(404)
def handle_not_found(error):

    print()
    print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
    print("ERRO 404")
    print("CAMINHO:", request.path, flush=True)
    print("MÉTODO:", request.method, flush=True)
    print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
    print()

    return {
        "success": False,
        "message": "Rota não encontrada.",
        "path": request.path
    }, 404


# =====================================================
# SECURITY CONFIG
# =====================================================

app.config.update(

    SESSION_COOKIE_HTTPONLY=True,

    SESSION_COOKIE_SECURE=False,

    SESSION_COOKIE_SAMESITE="Lax"

)


# =====================================================
# DEBUG - AMBIENTE
# =====================================================

print()
print("====================================================")
print("CONFIGURAÇÃO FINAL")
print("====================================================")

print(
    "PYTHON EXECUTÁVEL:",
    sys.executable,
    flush=True
)

print(
    "ARQUIVO APP:",
    __file__,
    flush=True
)

print(
    "SECRET KEY CONFIGURADA:",
    bool(app.secret_key),
    flush=True
)

print(
    "CSRF ATIVO:",
    True,
    flush=True
)

print(
    "WEB API URL:",
    "http://127.0.0.1:5001",
    flush=True
)

print(
    "WEB:",
    "http://127.0.0.1:5000",
    flush=True
)

print("====================================================")
print()


# =====================================================
# EXECUTAR SERVIDOR
# =====================================================

if __name__ == "__main__":

    print(
        "1️⃣5️⃣ INICIANDO SERVIDOR FLASK",
        flush=True
    )

    app.run(

        host="0.0.0.0",

        port=5000,

        debug=True

    )

