from requests import post
import psutil
from time import sleep
from socket import gethostname

import os
from dotenv import load_dotenv

load_dotenv()
GROUP_ID = os.getenv("GROUP_ID")
BOT_TOKEN = os.getenv("BOT_TOKEN")
hostname = gethostname()


def send(mssg: str):
    """This function sends the argument mssg to the telegram API"""
    post(f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage", data={'text': mssg, 'chat_id': GROUP_ID})

def cpu():
    MAX_CPU_USAGE = os.getenv("MAX_CPU_USAGE")
    cpu_usage = psutil.cpu_percent(interval=None)
    if cpu_usage >= MAX_CPU_USAGE:
        send(f"Warning! The system {hostname} is at {cpu_usage}%")
    
def users(prev: list):
    psusers = psutil.users()
    current = []
    for i in psusers:
        current.append(i.host)
        if i.host in ["localhost", None, ''] or i.host in prev:
            pass
        else:
            send(f"Alert! The system {hostname} detected a remote connection from {i.host} in {i.name}")
    print(prev, current)
    return current

def main():
    ip = []
    while True:
        cpu()
        ip = users(ip)
        sleep(1)

if __name__ == "__main__":
    main()