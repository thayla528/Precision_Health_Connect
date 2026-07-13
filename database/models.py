from database.bank import conectar


class ConviteModel:

    @staticmethod
    #Significa que não precisamos criar um objeto da classe.
    def criar(
        nome_completo,
        email,
        telefone,
        data_nascimento,
        tipo_perfil,
        motivo_interesse
    ):
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
            nome_completo,
            email,
            telefone,
            data_nascimento,
            tipo_perfil,
            motivo_interesse
        ))

        conn.commit()

        #retorna o id gerado automaticamente
        convite_id = cursor.lastrowid


        conn.close()

        return convite_id

    @staticmethod
    def buscar_por_email(email):

        conn = conectar()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT *
            FROM convites
            WHERE email = ?
        """, (email,))

        convite = cursor.fetchone()

        conn.close()

        return convite

    @staticmethod
    def buscar_por_codigo(codigo):

        conn = conectar()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT *
            FROM convites
            WHERE codigo_convite = ?
        """, (codigo,))

        convite = cursor.fetchone()

        conn.close()

        return convite

    @staticmethod
    def buscar_por_id(convite_id):

        conn = conectar()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT *
            FROM convites
            WHERE id = ?
        """, (convite_id,))

        convite = cursor.fetchone()

        conn.close()

        return convite

    @staticmethod
    def listar():

        conn = conectar()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT *
            FROM convites
            ORDER BY data_solicitacao DESC
        """)

        convites = cursor.fetchall()

        conn.close()

        return convites

    @staticmethod
    def aprovar(convite_id, codigo_convite, administrador_id):

        conn = conectar()
        cursor = conn.cursor()

        cursor.execute("""
            UPDATE convites
            SET
                status = ?,
                codigo_convite = ?,
                aprovado_por = ?,
                data_aprovacao = CURRENT_TIMESTAMP
            WHERE id = ?
        """, (
            "aprovado",
            codigo_convite,
            administrador_id,
            convite_id
        ))

        conn.commit()
        conn.close()

    @staticmethod
    def rejeitar(convite_id, administrador_id):

        conn = conectar()
        cursor = conn.cursor()

        cursor.execute("""
            UPDATE convites
            SET
                status = ?,
                aprovado_por = ?,
                data_aprovacao = CURRENT_TIMESTAMP
            WHERE id = ?
        """, (
            "rejeitado",
            administrador_id,
            convite_id
        ))

        conn.commit()
        conn.close()

    @staticmethod
    def listar_por_status(status):

        conn = conectar()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT *
            FROM convites
            WHERE status = ?
            ORDER BY data_solicitacao DESC
        """, (status,))

        convites = cursor.fetchall()

        conn.close()

        return convites

    @staticmethod
    def deletar(convite_id):

        conn = conectar()
        cursor = conn.cursor()

        cursor.execute("""
            DELETE FROM convites
            WHERE id = ?
        """, (convite_id,))

        conn.commit()
        conn.close()