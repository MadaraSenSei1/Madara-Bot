# main.py
from fastapi import FastAPI, Form, Query, HTTPException
from fastapi.responses import HTMLResponse, FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from bot.travian_bot import get_farm_lists, run_bot
import threading

app = FastAPI()

# 1) Serve our React/vanilla static bundle:
app.mount("/static", StaticFiles(directory="static"), name="static")

# 2) In‑memory session store:
user_sessions: dict[str, dict] = {}

# 3) Root: serve the index.html
@app.get("/", response_class=HTMLResponse)
async def index():
    return FileResponse("static/index.html")

# 4) Login endpoint (POST /login)
@app.post("/login")
async def login(
    username:   str = Form(...),
    password:   str = Form(...),
    server_url: str = Form(...),
    proxy_ip:   str = Form(""),
    proxy_port: str = Form(""),
    proxy_user: str = Form(""),
    proxy_pass: str = Form(""),
):
    user_sessions[username] = {
        "password":   password,
        "server_url": server_url,
        "proxy": {
            "ip":       proxy_ip,
            "port":     proxy_port,
            "username": proxy_user,
            "password": proxy_pass,
        }
    }
    return JSONResponse({"message": "Login saved"})

# 5) Farm‑list endpoint (GET /farmlist?username=...)
@app.get("/farmlist")
async def farmlist(username: str = Query(..., description="The username that previously logged in")):
    if username not in user_sessions:
        raise HTTPException(status_code=403, detail="Not logged in")
    conf = user_sessions[username]
    farms = get_farm_lists(
        username,
        conf["password"],
        conf["proxy"],
        conf["server_url"],
    )
    return JSONResponse({"farms": farms})

# 6) Start‑bot endpoint (POST /start-bot)
@app.post("/start-bot")
async def start_bot(
    username:     str = Form(...),
    interval_min: int = Form(...),
    interval_max: int = Form(...),
    random_secs:  bool = Form(False),
):
    if username not in user_sessions:
        raise HTTPException(status_code=403, detail="Not logged in")
    conf = user_sessions[username]
    # Launch in background so HTTP returns immediately
    threading.Thread(
        target=run_bot,
        args=(
            username,
            conf["password"],
            conf["proxy"],
            interval_min,
            interval_max,
            random_secs,
            conf["server_url"],
        ),
        daemon=True
    ).start()
    return JSONResponse({"message": "Bot started"})

# 7) If you ever need to run with Uvicorn directly:
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
