import time
from config import conectar_banco

def cadastrar_usuario():
    print("\n=== CADASTRAR USUÁRIO ===")
    print("1 - Artista")
    print("2 - Consumidor")
    print("3 - Cancelar")

    tipo = input("Escolha: ")

    if tipo == "3":
        return

    if tipo not in ("1", "2"):
        print("Opção inválida!")
        time.sleep(1)
        return

    nivel = "Artista" if tipo == "1" else "Consumidor"

    cpf = int(input("CPF (xxxxxxxxxxx): "))
    nome = input("Nome: ").strip()
    email = input("Email: ").strip()
    senha = input("Crie uma senha: ").strip()

    nome_artistico = None
    if nivel == "Artista":
        nome_artistico = input("Nome artístico: ").strip()

    try:
        conn = conectar_banco()
        cursor = conn.cursor()

        sql = """
            INSERT INTO Usuario (CPF, Nome, Nome_artistico, Email, Nivel_acesso, Senha)
            VALUES (%s, %s, %s, %s, %s, %s)
        """

        dados = (cpf, nome, nome_artistico, email, nivel, senha)

        cursor.execute(sql, dados)
        conn.commit()

        print("\n✅ Usuário cadastrado com sucesso!")
        time.sleep(1)

    except Exception as erro:
        print("\n❌ Erro ao cadastrar:", erro)
        time.sleep(2)

    finally:
        cursor.close()
        conn.close()


def login():
    print("\n=== LOGIN ===")
    email = input("Email: ").strip()
    senha = input("Senha: ").strip()

    try:
        conn = conectar_banco()
        cursor = conn.cursor()

        sql = """
            SELECT Id_usuario, Nivel_acesso
            FROM Usuario
            WHERE Email = %s AND Senha = %s
        """

        cursor.execute(sql, (email, senha))
        result = cursor.fetchone()

        if result:
            print("\nLogin realizado com sucesso!")
            time.sleep(1)
            return result  # (id_usuario, nivel_acesso)
        else:
            print("\n❌ Email ou senha incorretos.")
            time.sleep(1)
            return None

    except Exception as erro:
        print("Erro no login:", erro)
        return None

    finally:
        cursor.close()
        conn.close()
