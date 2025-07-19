from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse, JSONResponse
from bot.travian_bot import get_farm_lists
import uvicorn

app = FastAPI()

@app.get("/", response_class=HTMLResponse)
async def root():
    return """
    <html>
        <head>
            <title>Travian Bot</title>
        </head>
        <body style="font-family:sans-serif;text-align:center;margin-top:50px;">
            <h1>✅ Travian Bot läuft!</h1>
            <p>Backend ist bereit für API-Anfragen.</p>
            <p><code>/start_bot</code> erwartet POST-Daten.</p>
        </body>
    </html>
    """

@app.post("/start_bot")
async def start_bot(
    username: str = Form(...),
    password: str = Form(...),
    server_url: str = Form(...),
    proxy_ip: str = Form(""),
    proxy_port: str = Form(""),
    proxy_user: str = Form(""),
    proxy_pass: str = Form("")
):
    try:
        farm_lists = get_farm_lists(username, password, server_url, proxy_ip, proxy_port, proxy_user, proxy_pass)
        return JSONResponse(content={"status": "success", "data": farm_lists})
    except Exception as e:
        return JSONResponse(status_code=500, content={"status": "error", "message": str(e)})

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=10000)
