# backend/main.py

import os
import threading
import time
import random
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

# Umgebungsvariablen aus .env laden
load_dotenv()

app = FastAPI(title="Madara Farming Bot")

# Static‐Files (UI) ausliefern
app.mount("/", StaticFiles(directory="static", html=True), name="static")

# In‐Memory Speichergestell für Accounts & laufende Bots
accounts: dict[str, "Account"] = {}
threads: dict[str, threading.Thread] = {}

class Account(BaseModel):
    id: str
    username: str
    password: str
    server_url: str
    proxy_ip: str | None = None
    proxy_port: int | None = None
    proxy_user: str | None = None
    proxy_pass: str | None = None
    min_interval: int = 10
    max_interval: int = 15
    random_seconds: bool = False

@app.get("/api/accounts")
def list_accounts():
    return list(accounts.values())

@app.post("/api/accounts")
def add_account(acc: Account):
    if acc.id in accounts:
        raise HTTPException(status_code=400, detail="ID schon vorhanden")
    accounts[acc.id] = acc
    return {"status": "OK"}

@app.delete("/api/accounts/{acc_id}")
def del_account(acc_id: str):
    stop_bot(acc_id)
    accounts.pop(acc_id, None)
    return {"status": "gelöscht"}

@app.post("/api/start/{acc_id}")
def start_bot(acc_id: str):
    if acc_id not in accounts:
        raise HTTPException(404, "Account nicht gefunden")
    if acc_id in threads and threads[acc_id].is_alive():
        return {"status": "läuft bereits"}
    t = threading.Thread(target=bot_loop, args=(accounts[acc_id],), daemon=True)
    threads[acc_id] = t
    t.start()
    return {"status": "gestartet"}

@app.post("/api/stop/{acc_id}")
def stop_bot(acc_id: str):
    # wir nutzen da ein Flag in Account
    if acc_id not in accounts:
        raise HTTPException(404, "Account nicht gefunden")
    accounts[acc_id].stop = True
    return {"status": "gestoppt"}

@app.get("/api/status/{acc_id}")
def status(acc_id: str):
    running = acc_id in threads and threads[acc_id].is_alive()
    return {"running": running}

def bot_loop(acc: Account):
    """
    Beispiel‐Loop, hier solltest Du Deine Selenium‐Logik reinpacken.
    Das Flag `acc.stop = True` beendet den Loop.
    """
    acc.stop = False
    from bot.travian_bot import login_and_get_farms  # Deine Funktion dort

    while not getattr(acc, "stop", False):
        try:
            farms = login_and_get_farms(
                acc.username, acc.password, acc.server_url,
                acc.proxy_ip, acc.proxy_port, acc.proxy_user, acc.proxy_pass
            )
            print(f"[{acc.id}] Farm‑Liste:", farms)
        except Exception as e:
            print(f"[{acc.id}] Fehler beim Einloggen/Farms holen:", e)

        # warte zufällig zwischen min/max Minuten (und optional bis zu +30 s)
        secs = random.randint(acc.min_interval * 60, acc.max_interval * 60)
        if acc.random_seconds:
            secs += random.randint(0, 30)
        for i in range(secs, 0, -1):
            if acc.stop:
                break
            time.sleep(1)
    print(f"[{acc.id}] Bot beendet")
