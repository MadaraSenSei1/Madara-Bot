from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from bot.travian_bot import get_farm_lists

app = FastAPI()

# CORS aktivieren
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class LoginData(BaseModel):
    username: str
    password: str
    server_url: str
    proxy_ip: str = ""
    proxy_port: str = ""
    proxy_user: str = ""
    proxy_pass: str = ""

@app.post("/login")
async def login(data: LoginData):
    try:
        farm_lists = get_farm_lists(
            username=data.username,
            password=data.password,
            server_url=data.server_url,
            proxy_ip=data.proxy_ip,
            proxy_port=data.proxy_port,
            proxy_user=data.proxy_user,
            proxy_pass=data.proxy_pass
        )
        return {"success": True, "farmLists": farm_lists}
    except Exception as e:
        print("Login failed:", e)
        return {"success": False, "error": str(e)}
