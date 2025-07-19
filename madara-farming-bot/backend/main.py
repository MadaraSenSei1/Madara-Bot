# backend/main.py
import os, threading, time, random
from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from bot.travian_bot import login_and_fetch_farms, raid_one_farm

app = FastAPI(title="Madara Farming Bot")

# 1) Session‑Objekt für jeden Account
class Session:
    def __init__(self, cfg):
        self.id = cfg["id"]
        self.cfg = cfg
        self.farms = []
        self.running = False
        self.thread = None
        self.min_interval = cfg.get("min_interval", 10)
        self.max_interval = cfg.get("max_interval", 15)
        self.rand30 = cfg.get("rand30", False)
        self.next_wait = 0
        self.last_log = []

    def log(self, msg):
        ts = time.strftime("%H:%M:%S")
        self.last_log.insert(0, f"[{ts}] {msg}")
        if len(self.last_log)>50: self.last_log.pop()

    def start(self):
        if self.running: return
        self.running = True
        self.thread = threading.Thread(target=self._run_loop, daemon=True)
        self.thread.start()
        self.log("Bot gestartet")

    def stop(self):
        self.running = False
        self.log("Bot gestoppt")

    def _run_loop(self):
        try:
            # einmalig login + farm‑list
            self.log("Login + Farm‑List ziehen…")
            self.farms = login_and_fetch_farms(**self.cfg)
            self.log(f"{len(self.farms)} Farm(s) geladen")
            while self.running:
                iv = random.randint(self.min_interval, self.max_interval)*60
                if self.rand30: iv += random.randint(0,30)
                self.next_wait = iv
                self.log(f"Warte {iv//60}m{iv%60}s bis nächster Raid")
                # Countdown
                while self.running and self.next_wait>0:
                    time.sleep(1)
                    self.next_wait -=1
                if not self.running: break
                # Raid über alle Farmen
                for f in self.farms:
                    res = raid_one_farm(f, **self.cfg)
                    self.log(f"Raid auf {f['coords']}: {res['result']}")
        except Exception as e:
            self.log("Fehler: "+str(e))
            self.running = False

# 2) In‑Memory Store aller Sessions
SESSIONS = {}

# 3) Models
class AddAccount(BaseModel):
    username: str
    password: str
    server_url: str
    proxy_ip: str = None
    proxy_port: int = None
    proxy_user: str = None
    proxy_pass: str = None

class IntervalConfig(BaseModel):
    min_interval: int
    max_interval: int
    rand30: bool = False

# 4) Endpoints
@app.post("/api/accounts")
def add_account(cfg: AddAccount):
    idx = str(len(SESSIONS)+1)
    data = cfg.dict()
    data["id"]=idx
    sess = Session(data)
    SESSIONS[idx]=sess
    return {"id": idx}

@app.get("/api/accounts")
def list_accounts():
    return [
      {
        "id": s.id,
        "username": s.cfg["username"],
        "running": s.running,
        "next_wait": s.next_wait,
      } for s in SESSIONS.values()
    ]

@app.post("/api/accounts/{aid}/interval")
def set_interval(aid: str, iv: IntervalConfig):
    s = SESSIONS.get(aid)
    if not s: raise HTTPException(404,"No such session")
    s.min_interval, s.max_interval, s.rand30 = iv.min_interval, iv.max_interval, iv.rand30
    return {"ok":True}

@app.post("/api/accounts/{aid}/start")
def start_account(aid: str):
    s = SESSIONS.get(aid)
    if not s: raise HTTPException(404,"No such session")
    s.start()
    return {"running":True}

@app.post("/api/accounts/{aid}/stop")
def stop_account(aid: str):
    s = SESSIONS.get(aid)
    if not s: raise HTTPException(404,"No such session")
    s.stop()
    return {"running":False}

@app.get("/api/accounts/{aid}/status")
def status_account(aid: str):
    s = SESSIONS.get(aid)
    if not s: raise HTTPException(404,"No such session")
    return {
      "running": s.running,
      "next_wait": s.next_wait,
      "logs": s.last_log[:20]
    }

# 5) Statische UI ausliefern
app.mount("/", StaticFiles(directory="static", html=True), name="static")
