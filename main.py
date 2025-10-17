# Import necessary libraries
from pyfiglet import Figlet
import shutil
from colorama import Fore, Style, Back, init
import random
import socket
import threading

# Import key functions
import pgp
import broadcast
import scanner
import connect
from spinner import Spinner

# Global variables
TERMINAL_WIDTH = shutil.get_terminal_size().columns
VERSION = "0.1.0"

# Initialise colorama
init(autoreset=True)

# Printing the title
f = Figlet(font='epic')
title = f.renderText("Dark Chat")

for line in title.splitlines():
    print(Style.BRIGHT + line.center(TERMINAL_WIDTH) + Style.RESET_ALL)

print(("VERSION " + Style.BRIGHT + f"{VERSION}" + Style.RESET_ALL ).center(TERMINAL_WIDTH+8))
print(("DEVELOPED BY " + Style.BRIGHT + "ZAXN" + Style.RESET_ALL).center(TERMINAL_WIDTH+8))
print((Style.DIM + "mozaxn@protonmail.com" + Style.RESET_ALL).center(TERMINAL_WIDTH+8))
print("\n\n")
 
exists = 0
broadcast_port = random.randint(10_000, 65_001)
while True:

    # Broadcasting your availability to LAN
    if exists == 1:
        stop_event = threading.Event()
        t = threading.Thread(target=broadcast.broadcaster, args=(stop_event, broadcast_port), daemon=True)
        t.start()
    
    # Asking for input indefinitely
    command = input(Style.BRIGHT + Fore.BLUE + "cli@darkchat" + Style.RESET_ALL + ":" + Style.BRIGHT + Fore.BLUE + "~" + Style.RESET_ALL + Style.DIM + "$ " + Style.RESET_ALL)
    
    if command.strip() == '':
        continue
    
    # Exiting DarkChat
    if command == 'exit':
        if exists == 1:
            stop_event.set()
            t.join()
        break

    # Prompting for private key
    if command == 'init' and exists == 0:
        existing = input("Do you have any existing PRIVATE KEY provided by DarkChat? (Y/N): ")
        if existing.strip().upper() == "Y":
            
            sk_file = input("Enter the path to the PRIVATE KEY: ")
            passphrase = input("Enter PASSPHRASE: ")
            
            priv_key = pgp.find_priv_key(sk_file, passphrase)
            
            if priv_key == False:
                print(Style.BRIGHT + Back.RED + "[ERROR]" + Style.RESET_ALL + Fore.RED + " The file either doesn't exist or is corrupted!\n" + Style.RESET_ALL)
            else:
                print(Style.BRIGHT + Back.GREEN + "[SUCCESS]" + Style.RESET_ALL + "Found PRIVATE KEY! Fingerprint: " + Fore.BLUE + priv_key[0] + Style.RESET_ALL)
                exists = 1
        
        else:
            name = input("Enter your name: ")
            email = input("Enter your email: ")
            password = input("Enter your password for the PRIVATE KEY: ")
            
            fingerprint = pgp.create_pgp(name, email, passphrase=password)
            if fingerprint:
                print(Style.BRIGHT + Back.GREEN + "[SUCCESS]" + Style.RESET_ALL + " PGP Keys have been created. Key Fingerprint: " + Fore.BLUE + fingerprint + Style.RESET_ALL)
                exists = 1
            else:
                print(Style.BRIGHT + Back.RED + "[ERROR]" + Style.RESET_ALL + Fore.RED + "Couldn't create PGP Keys! Try again." + Style.RESET_ALL)
                
    elif command == 'init' and exists == 1:
        print("You already have loaded your PRIVATE KEY!")
        
    elif command == 'scan':
        with Spinner(message='Scanning network for DarkChat users...'):
            hosts = scanner.scanner()
        
        if len(hosts) == 0:
            print(Fore.YELLOW + "No active DarkChat users on the network! Try again.")
        else:
            print(f"Found {len(hosts)} active DarkChat user(s) on the network:")
            for host in hosts:
                print(Style.BRIGHT + Fore.BLUE + '- ' + Style.RESET_ALL + host)
    
    elif command.split()[0] == 'chat' and len(command.split()) == 2:
        host = command.split()[1]
        pub_key = open(input("Enter host's public key file: "), "r").read()
        connect.connection_req(host, 7887, pub_key)