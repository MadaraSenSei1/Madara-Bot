from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from bot.travian_bot import get_farm_lists
import uvicorn
import threading

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

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
        return {"success": False, "error": str(e)}
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
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
