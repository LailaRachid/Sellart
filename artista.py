# artista.py

import time
from config import conectar_banco

def menu_artista(id_artista):
    while True:
        print("\n====== MENU DO ARTISTA ======")
        print("1 - Criar / Editar Portfólio")
        print("2 - Criar Publicação (foto/vídeo)")
        print("3 - Editar / Excluir Publicação")
        print("4 - Ver Feedbacks Recebidos")
        print("5 - Voltar ao Menu Principal")

        try:
            op = int(input("Escolha: "))
        except ValueError:
            print("Opção inválida!")
            continue

        if op == 1:
            criar_ou_editar_portfolio(id_artista)

        elif op == 2:
            criar_publicacao(id_artista)

        elif op == 3:
            editar_ou_excluir_publicacao(id_artista)

        elif op == 4:
            ver_feedbacks(id_artista)

        elif op == 5:
            print("Voltando ao menu principal...")
            break

        else:
            print("Opção inválida!")


def criar_ou_editar_portfolio(id_artista):
    print("\n=== CRIAR / EDITAR PORTFÓLIO ===")

    sobre = input("Escreva sua descrição artística: ").strip()
    foto = input("URL da foto do portfólio: ").strip()

    try:
        conn = conectar_banco()
        cursor = conn.cursor()

        cursor.execute("SELECT Id_portifolio FROM Portifolio WHERE Id_usuario = %s", (id_artista,))
        existente = cursor.fetchone()

        if existente:
            sql = "UPDATE Portifolio SET Sobre_artista=%s, Foto_url=%s WHERE Id_usuario=%s"
            valores = (sobre, foto, id_artista)
            print("\nPortfólio atualizado!")
        else:
            sql = "INSERT INTO Portifolio (Id_usuario, Sobre_artista, Foto_url) VALUES (%s, %s, %s)"
            valores = (id_artista, sobre, foto)
            print("\nPortfólio criado!")

        cursor.execute(sql, valores)
        conn.commit()

    except Exception as e:
        print("Erro:", e)

    finally:
        cursor.close()
        conn.close()


def criar_publicacao(id_artista):
    print("\n=== CRIAR PUBLICAÇÃO ===")

    try:
        conn = conectar_banco()
        cursor = conn.cursor()

        cursor.execute("SELECT Id_portifolio FROM Portifolio WHERE Id_usuario=%s", (id_artista,))
        port = cursor.fetchone()

        if not port:
            print("❌ Você precisa criar um portfólio primeiro!")
            return

        id_port = port[0]

        desc = input("Descrição: ").strip()
        img = input("URL da imagem/vídeo: ").strip()
        tipo = input("Tipo de arte: ").strip()
      

        sql = """
            INSERT INTO Publicacao (Id_portifolio, Descricao, Imagem_url, Tipo_arte)
            VALUES (%s, %s, %s, %s)
        """
        cursor.execute(sql, (id_port, desc, img, tipo))
        conn.commit()

        print("\nPublicação criada com sucesso!")

    except Exception as e:
        print("Erro:", e)

    finally:
        cursor.close()
        conn.close()


def editar_ou_excluir_publicacao(id_artista):
    print("\n=== EDITAR / EXCLUIR PUBLICAÇÃO ===")

    try:
        conn = conectar_banco()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT P.Id_publicacao, P.Descricao
            FROM Publicacao P
            JOIN Portifolio F ON P.Id_portifolio = F.Id_portifolio
            WHERE F.Id_usuario = %s
        """, (id_artista,))

        pubs = cursor.fetchall()

        if not pubs:
            print("Nenhuma publicação encontrada.")
            return

        print("\nSuas publicações:")
        for pub in pubs:
            print(f"{pub[0]} - {pub[1]}")

        escolha = input("\nID da publicação: ")

        print("\n1 - Editar")
        print("2 - Excluir")
        acao = input("Escolha: ")

        if acao == "1":
            nova_desc = input("Nova descrição: ").strip()
            nova_img = input("Nova URL: ").strip()

            cursor.execute("""
                UPDATE Publicacao
                SET Descricao=%s, Imagem_url=%s
                WHERE Id_publicacao=%s
            """, (nova_desc, nova_img, escolha))

            conn.commit()
            print("\nPublicação atualizada!")

        elif acao == "2":
            cursor.execute("DELETE FROM Publicacao WHERE Id_publicacao=%s", (escolha,))
            conn.commit()
            print("\nPublicação removida!")

        else:
            print("Opção inválida!")

    except Exception as e:
        print("Erro:", e)

    finally:
        cursor.close()
        conn.close()


def ver_feedbacks(id_artista):
    print("\n=== FEEDBACKS RECEBIDOS ===")

    try:
        conn = conectar_banco()
        cursor = conn.cursor()
        
        cursor.execute("""
           SELECT F.Id_feedback, U.Nome, F.Comentario, F.Avaliacao
           FROM Feedback F
           JOIN Usuario U ON F.Id_consumidor = U.Id_usuario
           JOIN Portifolio P ON F.Id_publicacao = P.Id_portifolio
           WHERE P.Id_usuario = %s
        """, (id_artista,))


        dados = cursor.fetchall()

        if not dados:
            print("Nenhum feedback encontrado.")
            return

        print("\nFeedbacks:")
        for fb in dados:
            print(f"[{fb[0]}] {fb[1]} — Nota: {fb[3]}\n{fb[2]}\n")

    except Exception as e:
        print("Erro:", e)

    finally:
        cursor.close()
        conn.close()
    
