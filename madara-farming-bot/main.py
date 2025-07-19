from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse, JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from bot.travian_bot import login_and_save_session, get_farm_lists, start_farming_bot

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

user_sessions = {}

@app.get("/", response_class=HTMLResponse)
async def index():
    return FileResponse("static/index.html")


@app.post("/login")
async def login(
    username: str = Form(...),
    password: str = Form(...),
    server_url: str = Form(...),
    proxy_ip: str = Form(None),
    proxy_port: str = Form(None),
    proxy_user: str = Form(None),
    proxy_pass: str = Form(None)
):
    session = login_and_save_session(username, password, server_url, {
        "ip": proxy_ip,
        "port": proxy_port,
        "username": proxy_user,
        "password": proxy_pass
    })

    if session:
        user_sessions[username] = {
            "password": password,
            "server_url": server_url,
            "proxy": {
                "ip": proxy_ip,
                "port": proxy_port,
                "username": proxy_user,
                "password": proxy_pass
            },
            "session": session
        }
        return JSONResponse({"message": "Login successful"})
    else:
        return JSONResponse({"error": "Login failed"}, status_code=401)


@app.get("/farmlist")
async def get_farmlist(username: str):
    if username not in user_sessions:
        return JSONResponse({"error": "Not logged in"}, status_code=403)

    session_data = user_sessions[username]
    farm_lists = get_farm_lists(session_data["session"])
    return JSONResponse({"farms": farm_lists})


@app.post("/start-bot")
async def start_bot(
    username: str = Form(...),
    interval_min: int = Form(...),
    interval_max: int = Form(...),
    random_delay: bool = Form(False)
):
    session_data = user_sessions.get(username)
    if not session_data:
        return JSONResponse({"error": "Not logged in"}, status_code=403)

    start_farming_bot(session_data["session"], interval_min, interval_max, random_delay)
    return JSONResponse({"message": "Bot started"})
