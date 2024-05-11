# Welcome to the Generoso SDV-toolbox !

## Overview
The Generoso SDV-toolbox is a comprehensive Python toolkit designed to streamline pre-pentest operations. It supports a range of activities including DNS lookups, vulnerability assessments, reverse shell connections, password strength testing, and report generation.

## Installation
Clone the repository to get started with the Generoso SDV-toolbox:

    git clone https://github.com/Prxnkzy/sdv-toolbox.git
    
## Features
**Domain check-up**: Uses DNSPython to resolve nameservers for specified domains.

**Vulnerability scan**: Leverages Nmap for scanning ports and services, employing NSE scripts for detailed checks.

**Reverse shell**: Establishes reverse shell connections using Netcat, facilitating remote system access.

**Password analyzer**: Calculates the time required to brute-force a password, based on a study by Hive Systems.

**Reporting**: Automatically generates comprehensive reports detailing scan outcomes and security insights.

## Usage
**Domaine check-up**:
Enter a target IP address to retrieve the DNS, MX, and TXT records.

**Vulnerability scan**:
blabla

## Dependencies & licenses
**DNSPython**:

*Library: dns.resolver - Version: 2.6.1 - License: ISC*

**Nmap**:

*Library: subprocess (install the nmap module on nmap.org) - Version: 7.95 - License: Nmap Public Source License based on the GNU GPLv2*

**Netcat**:* 

*Library: socket (+install files on custom path for Windows 10) - Version: 1.12 - License: GNU GPL*

## Contact
For inquiries or potential collaborations, please reach out:
📧 Email: julien.generoso@supdevinci-edu.fr


