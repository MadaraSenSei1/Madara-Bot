from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse, FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from bot.travian_bot import get_farm_lists, run_bot

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

user_sessions = {}

@app.get("/", response_class=HTMLResponse)
async def serve_index():
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
        "server_url": server_url,
        "proxy": {
            "ip": proxy_ip,
            "port": proxy_port,
            "username": proxy_user,
            "password": proxy_pass
        }
    }
    return JSONResponse({"message": "Login gespeichert"})

@app.get("/farmlist")
async def get_farmlist(username: str):
    if username not in user_sessions:
        return JSONResponse({"error": "Nicht eingeloggt"}, status_code=403)

    session = user_sessions[username]
    farms = get_farm_lists(
        username,
        session["password"],
        session["proxy"],
        session["server_url"]
    )
    return JSONResponse({"farms": farms})

@app.post("/start-bot")
async def start_bot(
    username: str = Form(...),
    interval_min: int = Form(...),
    interval_max: int = Form(...)
):
    session = user_sessions.get(username)
    if not session:
        return JSONResponse({"error": "Nicht eingeloggt"}, status_code=403)

    run_bot(
        username,
        session["password"],
        session["proxy"],
        interval_min,
        interval_max,
        session["server_url"]
    )
    return JSONResponse({"message": "Bot gestartet"})

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=10000)
