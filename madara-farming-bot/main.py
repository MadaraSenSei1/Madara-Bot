# backend/main.py

import threading, uuid, os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from bot.travian_bot import get_farm_lists

app = FastAPI(title="Madara Farming Bot API")

# In‑Memory Store für Accounts und Status
ACCOUNTS = {}  # account_id → Account
STATUS   = {}  # account_id → {"running": bool, "last_farms": [...]}

class Account(BaseModel):
    username: str
    password: str
    server_url: str
    proxy_ip: str = ""
    proxy_port: str = ""
    proxy_user: str = ""
    proxy_pass: str = ""

@app.get("/accounts")
def list_accounts():
    return [{"id": aid, **acc.dict()} for aid, acc in ACCOUNTS.items()]

@app.post("/accounts", status_code=201)
def add_account(acc: Account):
    aid = str(uuid.uuid4())
    ACCOUNTS[aid] = acc
    STATUS[aid] = {"running": False, "last_farms": []}
    return {"id": aid}

@app.delete("/accounts/{aid}", status_code=204)
def delete_account(aid: str):
    if aid not in ACCOUNTS:
        raise HTTPException(404, "Account not found")
    # stoppe ggf. laufenden Thread
    STATUS.pop(aid, None)
    ACCOUNTS.pop(aid)
    return

@app.get("/accounts/{aid}/status")
def get_status(aid: str):
    if aid not in STATUS:
        raise HTTPException(404, "Account not found")
    return STATUS[aid]

@app.get("/accounts/{aid}/farmlists")
def fetch_farms(aid: str):
    if aid not in ACCOUNTS:
        raise HTTPException(404, "Account not found")
    acc = ACCOUNTS[aid]
    try:
        farms = get_farm_lists(**acc.dict())
        STATUS[aid]["last_farms"] = farms
        return {"farmlists": farms}
    except Exception as e:
        raise HTTPException(400, str(e))

def _bot_loop(aid: str, interval_sec: int):
    from time import sleep
    while STATUS[aid]["running"]:
        try:
            farms = get_farm_lists(**ACCOUNTS[aid].dict())
            STATUS[aid]["last_farms"] = farms
        except:
            pass
        sleep(interval_sec)

@app.post("/accounts/{aid}/start")
def start_bot(aid: str, interval: int = 600):
    if aid not in ACCOUNTS:
        raise HTTPException(404, "Account not found")
    if STATUS[aid]["running"]:
        raise HTTPException(400, "Already running")
    STATUS[aid]["running"] = True
    thread = threading.Thread(target=_bot_loop, args=(aid, interval), daemon=True)
    thread.start()
    return {"running": True}

@app.post("/accounts/{aid}/stop")
def stop_bot(aid: str):
    if aid not in ACCOUNTS:
        raise HTTPException(404, "Account not found")
    STATUS[aid]["running"] = False
    return {"running": False}
