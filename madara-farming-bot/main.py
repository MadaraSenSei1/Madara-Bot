from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from bot.travian_bot import get_farm_lists
import uvicorn

app = FastAPI()

# CORS erlauben
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # für Sicherheit besser Domains einschränken
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/login")
async def login(request: Request):
    data = await request.json()

    try:
        result = get_farm_lists(
            data["username"],
            data["password"],
            data["server_url"],
            data["proxy_ip"],
            data["proxy_port"],
            data["proxy_user"],
            data["proxy_pass"]
        )
        return JSONResponse(content={"success": True, "result": result})
    except Exception as e:
        return JSONResponse(content={"success": False, "error": str(e)})

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=10000)
