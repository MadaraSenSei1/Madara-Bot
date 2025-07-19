# main.py

from fastapi import FastAPI, Request, Form
from fastapi.responses import JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from bot.travian_bot import get_farm_lists
import traceback

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
def get_index():
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
    try:
        farm_lists = get_farm_lists(
            username=username,
            password=password,
            server_url=server_url,
            proxy_ip=proxy_ip,
            proxy_port=proxy_port,
            proxy_user=proxy_user,
            proxy_pass=proxy_pass
        )
        return {"success": True, "farm_lists": farm_lists}
    except Exception as e:
        error_trace = traceback.format_exc()
        print("ERROR during login:\n", error_trace)
        return JSONResponse(content={"success": False, "error": str(e)}, status_code=500)
