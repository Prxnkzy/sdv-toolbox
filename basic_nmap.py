# Options du menu : NMAP

def scan_de_port():
    print("Option 1 : Découverte de ports")
    print("Veuillez entrer l'adresse IP ou le nom de domaine à scanner :")
    cible = input("> ")
    
    # Commande Nmap
    commande_nmap = ["nmap", "-Pn", "-p-", "-sV", cible]
    
    # Exécution
    try:
        resultat = subprocess.run(commande_nmap, capture_output=True, text=True, check=True)
        # Affichage du résultat
        print(resultat.stdout)
    except subprocess.CalledProcessError as e:
        # Message d'erreur
        print("Erreur lors de l'exécution de la commande Nmap :", e)