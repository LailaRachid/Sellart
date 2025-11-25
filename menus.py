import time
from usuarios import cadastrar_usuario, login
from artista import menu_artista
from consumidor import menu_consumidor

def menu_principal():
    while True:
        print("\n====== MENU PRINCIPAL ======")
        print("1 - Cadastrar Usuário")
        print("2 - Login")
        print("3 - Sair")
        print("============================")

        opcao = input("Escolha: ")

        if opcao == "1":
            cadastrar_usuario()

        elif opcao == "2":
            dados = login()  # retorna (id_usuario, tipo)

            if dados is None:
                print("Login falhou.")
                time.sleep(1)
                continue

            user_id, tipo = dados

            if tipo == "Artista":
                menu_artista(user_id)
            elif tipo == "Consumidor":
                menu_consumidor(user_id)
            elif tipo == "Administrador":
                menu_admin()

        elif opcao == "3":
            print("Saindo...")
            time.sleep(1)
            break

        else:
            print("Opção inválida!")
            time.sleep(1)

if __name__ == "__main__":
    menu_principal()
