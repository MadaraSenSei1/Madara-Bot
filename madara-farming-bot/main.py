from fastapi import FastAPI, Form, UploadFile, Request
from fastapi.responses import JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn
import asyncio
from bot.travian_bot import login_and_get_farms, start_farming_bot

app = FastAPI()

# Static files (HTML, CSS, JS)
app.mount("/", StaticFiles(directory="static", html=True), name="static")

# Enable CORS if needed (e.g. for local frontend testing)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Store sessions in memory (you can switch to DB later)
user_sessions = {}

@app.post("/login")
async def login(
    username: str = Form(...),
    password: str = Form(...),
    server_url: str = Form(...),
    proxy_ip: str = Form(""),
    proxy_port: str = Form(""),
    proxy_user: str = Form(""),
    proxy_pass: str = Form("")
):
    proxy = {
        "ip": proxy_ip,
        "port": proxy_port,
        "username": proxy_user,
        "password": proxy_pass
    }

    try:
        farms = login_and_get_farms(username, password, server_url, proxy)
        user_sessions[username] = {
            "username": username,
            "password": password,
            "server_url": server_url,
            "proxy": proxy,
            "farms": farms
        }
        return {"status": "ok"}
    except Exception as e:
        return JSONResponse(status_code=400, content={"error": str(e)})

@app.get("/farmlist")
async def get_farm_lists(username: str):
    session = user_sessions.get(username)
    if not session:
        return JSONResponse(status_code=403, content={"error": "Not logged in"})

    try:
        farms = login_and_get_farms(session["username"], session["password"], session["server_url"], session["proxy"])
        session["farms"] = farms
        return {"farms": farms}
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})

@app.post("/start-bot")
async def start_bot(
    username: str = Form(...),
    interval_min: int = Form(...),
    interval_max: int = Form(...),
    random_delay: bool = Form(...)
):
    session = user_sessions.get(username)
    if not session:
        return JSONResponse(status_code=403, content={"error": "Not logged in"})

    try:
        next_run = await start_farming_bot(
            username=session["username"],
            password=session["password"],
            server_url=session["server_url"],
            proxy=session["proxy"],
            interval_min=interval_min,
            interval_max=interval_max,
            randomize=random_delay
        )
        return {"status": "started", "next_run_seconds": next_run}
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})

# Local testing (optional)
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=10000)
