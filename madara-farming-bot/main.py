from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse, FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from bot.travian_bot import get_farm_lists, run_bot
import threading

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

# In‑memory user sessions
user_sessions = {}

@app.get("/", response_class=HTMLResponse)
async def index():
    return FileResponse("static/index.html")

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
    user_sessions[username] = {
        "password": password,
        "server_url": server_url.rstrip("/"),
        "proxy": {
            "ip": proxy_ip,
            "port": proxy_port,
            "username": proxy_user,
            "password": proxy_pass
        }
    }
    return JSONResponse({"message": "Login successful"})

@app.get("/farmlist")
async def farmlist(username: str):
    if username not in user_sessions:
        return JSONResponse({"error": "Not logged in"}, status_code=403)
    sess = user_sessions[username]
    farms = get_farm_lists(
        username,
        sess["password"],
        sess["server_url"],
        sess["proxy"]
    )
    return JSONResponse({"farms": farms})

@app.post("/start-bot")
async def start_bot(
    username: str = Form(...),
    interval_min: int = Form(...),
    interval_max: int = Form(...),
    random_delay: bool = Form(False)
):
    if username not in user_sessions:
        return JSONResponse({"error": "Not logged in"}, status_code=403)
    sess = user_sessions[username]
    # launch background thread
    threading.Thread(
        target=run_bot,
        args=(
            username,
            sess["password"],
            sess["server_url"],
            sess["proxy"],
            interval_min,
            interval_max,
            random_delay
        ),
        daemon=True
    ).start()
    return JSONResponse({"message": "Bot started"})

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=10000)
