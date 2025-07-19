from fastapi import FastAPI, Form, Query, HTTPException
from fastapi.responses import HTMLResponse, FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from bot.travian_bot import get_farm_lists, run_bot
import threading

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
    proxy_ip: str = Form(""),
    proxy_port: str = Form(""),
    proxy_user: str = Form(""),
    proxy_pass: str = Form(""),
):
    try:
        # Attempt to login using TravianBot
        farm_lists = get_farm_lists(username, password, server_url, proxy_ip, proxy_port, proxy_user, proxy_pass)

        # Save session
        user_sessions[username] = {
            "password": password,
            "server_url": server_url,
            "proxy": {
                "ip": proxy_ip,
                "port": proxy_port,
                "username": proxy_user,
                "password": proxy_pass
            }
        }

        return JSONResponse({"message": "ok", "farm_lists": farm_lists})
    
    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=502)


@app.get("/farmlist")
async def get_farmlist(username: str = Query(...)):
    if username not in user_sessions:
        raise HTTPException(status_code=401, detail="Not logged in")

    conf = user_sessions[username]

    try:
        farms = get_farm_lists(
            username,
            conf["password"],
            conf["server_url"],
            conf["proxy"]["ip"],
            conf["proxy"]["port"],
            conf["proxy"]["username"],
            conf["proxy"]["password"]
        )
        return farms

    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=500)


@app.post("/start")
async def start_bot(
    username: str = Form(...),
    min_interval: int = Form(...),
    max_interval: int = Form(...),
    randomize: bool = Form(...)
):
    if username not in user_sessions:
        raise HTTPException(status_code=401, detail="Not logged in")

    conf = user_sessions[username]

    def run():
        run_bot(
            username,
            conf["password"],
            conf["server_url"],
            min_interval,
            max_interval,
            randomize,
            conf["proxy"]["ip"],
            conf["proxy"]["port"],
            conf["proxy"]["username"],
            conf["proxy"]["password"]
        )

    thread = threading.Thread(target=run)
    thread.start()

    return {"message": "Bot started"}
