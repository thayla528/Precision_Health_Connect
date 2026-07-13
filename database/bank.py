import sqlite3


def conectar():
    conn = sqlite3.connect("database/health.db")
    conn.row_factory = sqlite3.Row

    conn.execute("PRAGMA foreign_keys = ON")

    return conn


def criar_tabelas():
    conn = conectar()
    cursor = conn.cursor()

    # ---------------- TABELA DE CONVITES ----------------
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS convites (
            id INTEGER PRIMARY KEY AUTOINCREMENT,

            nome_completo TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            telefone TEXT,

            data_nascimento DATE,

            tipo_perfil TEXT NOT NULL,

            motivo_interesse TEXT,

            codigo_convite TEXT UNIQUE,

            status TEXT DEFAULT 'pendente',

            aprovado_por INTEGER,

            data_solicitacao DATETIME DEFAULT CURRENT_TIMESTAMP,

            data_aprovacao DATETIME,

            FOREIGN KEY(aprovado_por)
                REFERENCES administradores(id)
        )
    """)

    # ---------------- TABELA DE USUÁRIOS ----------------
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,

            convite_id INTEGER,

            nome_completo TEXT NOT NULL,

            email TEXT UNIQUE NOT NULL,

            senha TEXT NOT NULL,

            tipo_perfil TEXT NOT NULL,

            foto_perfil TEXT,

            ativo INTEGER DEFAULT 1,

            ultimo_login DATETIME,

            data_criacao DATETIME DEFAULT CURRENT_TIMESTAMP,

            FOREIGN KEY(convite_id)
                REFERENCES convites(id)
        )
    """)

    # ---------------- TABELA DE PACIENTES ----------------
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS pacientes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,

            usuario_id INTEGER UNIQUE NOT NULL,

            cpf TEXT,

            sexo TEXT,

            tipo_sanguineo TEXT,

            cep TEXT,

            endereco TEXT,

            numero TEXT,

            complemento TEXT,

            bairro TEXT,

            cidade TEXT,

            estado TEXT,

            observacoes TEXT,

            data_cadastro DATETIME DEFAULT CURRENT_TIMESTAMP,

            FOREIGN KEY(usuario_id)
                REFERENCES usuarios(id)
        )
    """)

    # ---------------- TABELA DE PROFISSIONAIS ----------------
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS profissionais (
            id INTEGER PRIMARY KEY AUTOINCREMENT,

            usuario_id INTEGER UNIQUE NOT NULL,

            especialidade TEXT NOT NULL,

            registro_profissional TEXT UNIQUE NOT NULL,

            instituicao TEXT,

            area_atuacao TEXT,

            telefone TEXT,

            email_profissional TEXT,

            ativo INTEGER DEFAULT 1,

            data_cadastro DATETIME DEFAULT CURRENT_TIMESTAMP,

            FOREIGN KEY(usuario_id)
                REFERENCES usuarios(id)
        )
    """)

    # ---------------- TABELA DE ADMINISTRADORES ----------------
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS administradores (
            id INTEGER PRIMARY KEY AUTOINCREMENT,

            usuario_id INTEGER UNIQUE NOT NULL,

            nivel_acesso TEXT DEFAULT 'admin',

            setor TEXT,

            data_cadastro DATETIME DEFAULT CURRENT_TIMESTAMP,

            FOREIGN KEY(usuario_id)
                REFERENCES usuarios(id)
        )
    """)

    # ---------------- TABELA DE CONSULTAS ----------------
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS consultas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,

            paciente_id INTEGER NOT NULL,

            profissional_id INTEGER NOT NULL,

            data_consulta DATETIME NOT NULL,

            motivo_consulta TEXT,

            status TEXT DEFAULT 'agendada',

            link_reuniao TEXT,

            observacoes TEXT,

            data_criacao DATETIME DEFAULT CURRENT_TIMESTAMP,

            FOREIGN KEY(paciente_id)
                REFERENCES pacientes(id),

            FOREIGN KEY(profissional_id)
                REFERENCES profissionais(id)
        )
    """)

    # ---------------- TABELA DE REGISTROS CLÍNICOS ----------------
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS registros_clinicos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,

            consulta_id INTEGER NOT NULL,

            diagnostico TEXT,

            tratamento TEXT,

            prescricao TEXT,

            observacoes TEXT,

            data_registro DATETIME DEFAULT CURRENT_TIMESTAMP,

            FOREIGN KEY(consulta_id)
                REFERENCES consultas(id)
        )
    """)

    # ---------------- TABELA DE DOCUMENTOS MÉDICOS ----------------
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS documentos_medicos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,

            paciente_id INTEGER NOT NULL,

            enviado_por INTEGER,

            nome_arquivo TEXT NOT NULL,

            tipo_documento TEXT,

            caminho_arquivo TEXT NOT NULL,

            data_upload DATETIME DEFAULT CURRENT_TIMESTAMP,

            FOREIGN KEY(paciente_id)
                REFERENCES pacientes(id),

            FOREIGN KEY(enviado_por)
                REFERENCES usuarios(id)
        )
    """)

    # ---------------- TABELA DE NOTIFICAÇÕES ----------------
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS notificacoes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,

            usuario_id INTEGER NOT NULL,

            tipo TEXT,

            titulo TEXT NOT NULL,

            mensagem TEXT NOT NULL,

            lida INTEGER DEFAULT 0,

            data_envio DATETIME DEFAULT CURRENT_TIMESTAMP,

            FOREIGN KEY(usuario_id)
                REFERENCES usuarios(id)
        )
    """)

    # ---------------- TABELA DE MENSAGENS ----------------
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS mensagens (
            id INTEGER PRIMARY KEY AUTOINCREMENT,

            remetente_id INTEGER NOT NULL,

            destinatario_id INTEGER NOT NULL,

            mensagem TEXT NOT NULL,

            lida INTEGER DEFAULT 0,

            data_envio DATETIME DEFAULT CURRENT_TIMESTAMP,

            FOREIGN KEY(remetente_id)
                REFERENCES usuarios(id),

            FOREIGN KEY(destinatario_id)
                REFERENCES usuarios(id)
        )
    """)

    # ---------------- TABELA DE LOGS DE SEGURANÇA ----------------
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS logs_seguranca (
            id INTEGER PRIMARY KEY AUTOINCREMENT,

            usuario_id INTEGER,

            acao TEXT NOT NULL,

            ip TEXT,

            navegador TEXT,

            dispositivo TEXT,

            data_hora DATETIME DEFAULT CURRENT_TIMESTAMP,

            FOREIGN KEY(usuario_id)
                REFERENCES usuarios(id)
        )
    """)

    conn.commit()
    conn.close()


if __name__ == "__main__":
    criar_tabelas()
    print("Banco criado com sucesso!")