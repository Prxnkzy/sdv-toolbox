# Welcome to the Generoso SDV-toolbox !

## Overview
The Generoso SDV-toolbox is a comprehensive Python toolkit designed to streamline pre-pentest operations. It supports a range of activities including DNS lookups, ARP scan, vulnerability assessments, reverse shell connections, and report generation.

## Installation
Clone the repository to get started with the Generoso SDV-toolbox:

    git clone https://github.com/Prxnkzy/sdv-toolbox.git
    
## Features
**Domain check-up**: Uses DNSPython to resolve nameservers for specified domains.

**ARP scan** : With Scapy, discover the IP addresses and their corresponding MAC addresses on a chosen network.

**Vulnerability scan**: Leverages Nmap for scanning ports and services, employing NSE scripts for detailed checks.

**Reverse shell**: Establishes reverse shell connections using Netcat, facilitating remote system access.

**Auto-reporting**: Automatically generates comprehensive reports detailing the previous execution of the code with DualWriter.

## Usage
**Domaine check-up**:
Enter a target IP address to retrieve the DNS, MX, and TXT records.

**ARP scan**:
Enter a target network to resolve IP address and MAC address.

**Vulnerability scan**:
Enter a target IP address to scan, the attack level, and the ports.
+ *-Pn: Disables the ping phase, treating the host as active.*
+ *-T: Specifies the scan's aggression level (1 being the slowest and stealthiest, 5 being the fastest and noisiest).*
+ *-sV: Service version detection.*
+ *--script=vuln: Executes vulnerability detection scripts (NSE).*

**Reserve shell**:
Enter a target IP address and a listening port to establish a connection and inject commands. Change the path in *'commande_netcat'* according to your operating system (default *"C:\netcat-win32-1.12\nc.exe")*
+ *-l: Listen mode.*
+ *-v: Vebose mode.*
+ *-p: Specifies the port to listen on.*
+ *-e cmd.exe: Executes 'cmd.exe' after establishing the connection.*

**Auto-reporting**:
The DualWriter class redirects text output to multiple destinations simultaneously. It behaves like a file object, making it compatible with sys.stdout or other open files.
When you apply the *log_to_file* decorator using *@log_to_file*, each function execution is logged to *logs.txt* while displaying outputs in the console.
+ Backs up the console output
+ Opens or creates *logs.txt* without overwriting old records
+ Writes a timestamp in the logs before running the function
+ Redirects text to both the console and the file
+ Restores the original console output

## Dependencies & licenses
**DNSPython**:
+ *Libraries dns.resolver and socket*
+ *Version 2.6.1*
+ *ISC license*

**Scapy**:
+ *Libraries ARP, Ether et srp (from Scapy) + Npcap installation*
+ *Version 2.5.0*
+ *GNU GPL license*

**Nmap**:
+ *Library subprocess (+install the nmap module on nmap.org)*
+ *Version 7.95*
+ *Nmap Public Source License based on the GNU GPLv2*

**Netcat**:
+ *Libraries subprocess, threading, and time (+install netcat files on custom path for Windows 10)*
+ *Version 1.12*
+ *GNU GPL license*

**Auto-reporting**:
+ *Libraries datetime and sys*
+ *No licences*

## Contact
For inquiries or potential collaborations, please reach out:
📧 Email: julien.generoso@supdevinci-edu.fr


