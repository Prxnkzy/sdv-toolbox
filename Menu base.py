#Generoso SDV-toolbox v2024

import subprocess



# Menu principal
def afficher_menu():
    print("\n------ Bienvenue sur Generoso SDV-toolbox v2024 ------")
    print( )
    print("1. Scan de ports basique")
    print("0. Quitter")



# Fonction principale pour exécuter le menu
def executer_menu():
    while True:
        afficher_menu()
        choix = input("Choisissez une option : ")
        if choix == "1":
            scan_de_port()
        elif choix == "0":
            print("Au revoir !")
            break
        else:
            print("Veuillez entrer un nombre entre 0 et ....")



# Exécution du menu
if __name__ == "__main__":
    executer_menu()