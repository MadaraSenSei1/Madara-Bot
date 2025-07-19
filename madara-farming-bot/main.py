
from fastapi import FastAPI, Form
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from bot.travian_bot import get_farm_lists, run_bot
import uvicorn

app = FastAPI()
app.mount("/", StaticFiles(directory="static", html=True), name="static")

sessions = {}

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
    try:
        session = login_and_save_session(username, password, server_url, {
            "ip": proxy_ip,
            "port": proxy_port,
            "username": proxy_user,
            "password": proxy_pass
        })
        sessions[username] = session
        return {"success": True}
    except Exception as e:
        return JSONResponse(status_code=400, content={"error": str(e)})

@app.get("/farmlist")
async def farm_list(username: str):
    if username not in sessions:
        return JSONResponse(status_code=403, content={"error": "Not logged in"})
    try:
        farms = get_farm_lists(sessions[username])
        return {"farms": farms}
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})

@app.post("/start-bot")
async def start_bot(username: str = Form(...), interval_min: int = Form(...), interval_max: int = Form(...)):
    if username not in sessions:
        return JSONResponse(status_code=403, content={"error": "Not logged in"})
    try:
        start_farming_bot(sessions[username], interval_min, interval_max)
        return {"success": True}
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=10000)
