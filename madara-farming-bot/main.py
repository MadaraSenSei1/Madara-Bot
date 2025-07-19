from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse, JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from bot.travian_bot import run_bot, get_farm_lists
import os

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
    proxy_ip: str = Form(...),
    proxy_port: str = Form(...),
    proxy_user: str = Form(...),
    proxy_pass: str = Form(...)
):
    user_sessions[username] = {
        "password": password,
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
    password = session["password"]
    proxy = session["proxy"]

    # Call bot logic to scrape farm list
    try:
        farms = get_farm_lists(username, password, proxy)
        return JSONResponse({"farms": farms})
    except Exception as e:
        return JSONResponse({"error": f"Fehler beim Abrufen der Farmliste: {str(e)}"}, status_code=500)

@app.post("/start-bot")
async def start_bot(
    username: str = Form(...),
    interval_min: int = Form(...),
    interval_max: int = Form(...)
):
    session = user_sessions.get(username)
    if not session:
        return JSONResponse({"error": "Nicht eingeloggt"}, status_code=403)

    password = session["password"]
    proxy = session["proxy"]

    run_bot(username, password, proxy, interval_min, interval_max)
    return JSONResponse({"message": "Bot gestartet!"})

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=10000)
