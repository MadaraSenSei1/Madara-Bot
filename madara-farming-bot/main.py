from fastapi import FastAPI, Form
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from starlette.requests import Request
from bot.travian_bot import get_farm_lists

app = FastAPI()

# Static files (HTML)
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
async def root():
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
    try:
        farms = get_farm_lists(username, password, server_url, proxy_ip, proxy_port, proxy_user, proxy_pass)
        return {"success": True, "farm_lists": farms}
    except Exception as e:
        return JSONResponse(content={"success": False, "error": str(e)}, status_code=400)
