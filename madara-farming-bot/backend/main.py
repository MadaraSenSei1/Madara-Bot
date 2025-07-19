from fastapi import FastAPI, Request, BackgroundTasks
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel
from bot.travian_bot import TravianBot
import uvicorn
import uuid

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

# Alle aktiven Bots (key = account_id)
bots = {}

class LoginRequest(BaseModel):
    username: str
    password: str
    server: str
    proxy: str = None
    proxy_user: str = None
    proxy_pass: str = None

class BotSettings(BaseModel):
    account_id: str
    min_interval: int
    max_interval: int
    random_offset: bool

@app.get("/", response_class=HTMLResponse)
async def root():
    with open("static/index.html", "r") as f:
        return f.read()

@app.post("/login")
async def login(data: LoginRequest):
    account_id = str(uuid.uuid4())
    bot = TravianBot(
        username=data.username,
        password=data.password,
        server_url=data.server,
        proxy=data.proxy,
        proxy_user=data.proxy_user,
        proxy_pass=data.proxy_pass
    )

    try:
        farm_lists = bot.login_and_fetch_farm_lists()
        bots[account_id] = bot
        return {"success": True, "account_id": account_id, "farm_lists": farm_lists}
    except Exception as e:
        return JSONResponse(status_code=400, content={"success": False, "error": str(e)})

@app.post("/start_bot")
async def start_bot(settings: BotSettings, tasks: BackgroundTasks):
    account_id = settings.account_id
    if account_id not in bots:
        return JSONResponse(status_code=404, content={"success": False, "error": "Account not found"})

    bot = bots[account_id]
    bot.set_interval(settings.min_interval, settings.max_interval, settings.random_offset)

    # Starte Bot im Hintergrund
    tasks.add_task(bot.start_farming_loop)
    return {"success": True, "message": "Bot started"}

@app.post("/stop_bot")
async def stop_bot(data: dict):
    account_id = data.get("account_id")
    if account_id in bots:
        bots[account_id].stop()
        return {"success": True}
    return JSONResponse(status_code=404, content={"success": False, "error": "Bot not running"})

@app.get("/status/{account_id}")
async def get_status(account_id: str):
    if account_id in bots:
        bot = bots[account_id]
        return {
            "running": bot.running,
            "next_raid_in": bot.get_remaining_time()
        }
    return JSONResponse(status_code=404, content={"success": False, "error": "Account not found"})

if __name__ == "__main__":
    uvicorn.run("backend.main:app", host="0.0.0.0", port=10000, reload=True)
