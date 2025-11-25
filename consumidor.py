# consumidor.py
import time
from config import conectar_banco

def menu_consumidor(id_consumidor):
    while True:
        print("\n====== MENU DO CONSUMIDOR ======")
        print("1 - Visualizar publicações")
        print("2 - Enviar Feedback para Artista")
        print("3 - Sair")
        print("=================================")

        opc = input("Escolha: ")

        if opc == "1":
            visualizar_publicacoes()
        elif opc == "2":
            enviar_feedback(id_consumidor)
        elif opc == "3":
            break
        else:
            print("Opção inválida!")
            time.sleep(1)


def visualizar_publicacoes():
    print("\n=== TODAS AS PUBLICAÇÕES ===")

    try:
        conn = conectar_banco()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT Id_publicacao, Descricao, Imagem_url, Data_publicacao, Tipo_arte
            FROM Publicacao
        """)

        resultados = cursor.fetchall()

        if not resultados:
            print("Nenhuma publicação encontrada.")
            return

        for pub in resultados:
            print(f"\nID: {pub[0]}")
            print(f"Descrição: {pub[1]}")
            print(f"Imagem: {pub[2]}")
            print(f"Data: {pub[3]}")
            print(f"Tipo de Arte: {pub[4]}")
            print("----------------------")

    except Exception as erro:
        print("Erro ao buscar publicações:", erro)

    finally:
        cursor.close()
        conn.close()

    input("\nPressione ENTER para continuar...")

def enviar_feedback(id_consumidor):
    print("\n=== ENVIAR FEEDBACK ===")
    id_publicacao = input("ID da publicação: ").strip()
    avaliacao = int (input("Nota (de 1 a 5):"))
    comentario = input("Seu feedback: ").strip()

    try:
        conn = conectar_banco()
        cursor = conn.cursor()

        sql = """
            INSERT INTO Feedback (Id_publicacao,Avaliacao, comentario, Id_consumidor)
            VALUES (%s,%s, %s, %s)
        """

        cursor.execute(sql, (id_publicacao,avaliacao, comentario, id_consumidor))
        conn.commit()

        print("\nFeedback enviado com sucesso!")

    except Exception as erro:
        print("Erro ao enviar feedback:", erro)

    finally:
        cursor.close()
        conn.close()
    input("\nPressione ENTER para continuar...")

