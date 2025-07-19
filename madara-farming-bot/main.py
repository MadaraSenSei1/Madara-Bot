from fastapi import FastAPI, Request, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from bot.travian_bot import get_farm_lists
import uvicorn
import threading

app = FastAPI()

# Middleware für CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# 👉 Static Files mounten
app.mount("/static", StaticFiles(directory="static"), name="static")

# 👉 index.html bei Root-Route ausliefern
@app.get("/")
async def root():
    return FileResponse("static/index.html")


from fastapi import FastAPI, Request
import traceback

@app.post("/login")
async def login(request: Request):
    data = await request.json()
    try:
        farm_lists = get_farm_lists(
            username=data["username"],
            password=data["password"],
            server_url=data["server_url"],
            proxy_ip=data["proxy_ip"],
            proxy_port=data["proxy_port"],
            proxy_user=data["proxy_user"],
            proxy_pass=data["proxy_pass"]
        )
        return {"success": True, "farmLists": farm_lists}
    except Exception as e:
        # WICHTIG: Fehlerausgabe für Debugging
        print("=== LOGIN ERROR ===")
        traceback.print_exc()
        return {"success": False, "error": str(e)}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
