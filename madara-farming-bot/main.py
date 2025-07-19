from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import asyncio
import random
import threading

from travian_bot import login_and_fetch_farms, run_farming_bot

app = FastAPI()

# CORS für dein HTML-Frontend zulassen
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Globale Variablen zur Zwischenspeicherung
session_data = {}
bot_thread = None

# Datenmodelle
class LoginData(BaseModel):
    username: str
    password: str
    server_url: str
    proxy: dict

class BotInterval(BaseModel):
    interval_min: int
    interval_max: int

@app.post("/login")
async def login(data: LoginData):
    try:
        farms = login_and_fetch_farms(
            data.username, data.password, data.server_url, data.proxy
        )
        session_data["username"] = data.username
        session_data["password"] = data.password
        session_data["server_url"] = data.server_url
        session_data["proxy"] = data.proxy
        session_data["farms"] = farms
        return {"success": True, "farms": farms}
    except Exception as e:
        return {"success": False, "error": str(e)}

@app.get("/get-farms")
async def get_farms():
    try:
        farms = login_and_fetch_farms(
            session_data["username"],
            session_data["password"],
            session_data["server_url"],
            session_data["proxy"]
        )
        session_data["farms"] = farms
        return {"farms": farms}
    except Exception as e:
        return {"error": str(e)}

@app.post("/start-bot")
async def start_bot(interval: BotInterval):
    try:
        def bot_loop():
            while True:
                wait_minutes = random.randint(interval.interval_min, interval.interval_max)
                wait_seconds = random.randint(0, 30)
                total_seconds = wait_minutes * 60 + wait_seconds

                run_farming_bot(
                    session_data["username"],
                    session_data["password"],
                    session_data["server_url"],
                    session_data["proxy"]
                )
                asyncio.run(asyncio.sleep(total_seconds))

        global bot_thread
        if bot_thread and bot_thread.is_alive():
            return {"message": "Bot already running"}
        bot_thread = threading.Thread(target=bot_loop, daemon=True)
        bot_thread.start()

        return {"status": "started", "next_delay_seconds": interval.interval_min * 60 + random.randint(0, 30)}
    except Exception as e:
        return {"error": str(e)}
