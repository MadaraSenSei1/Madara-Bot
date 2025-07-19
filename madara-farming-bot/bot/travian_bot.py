# bot/travian_bot.py

import requests
from typing import List, Dict

def get_farm_lists(
    username: str,
    password: str,
    server_url: str,
    proxy_ip: str = "",
    proxy_port: str = "",
    proxy_user: str = "",
    proxy_pass: str = ""
) -> List[Dict]:
    """
    Loggt sich in Travian ein und gibt die Farm‑Listen zurück.
    """

    session = requests.Session()

    # Proxy konfigurieren (optional)
    if proxy_ip and proxy_port:
        proxy_url = f"http://{proxy_user}:{proxy_pass}@{proxy_ip}:{proxy_port}"
        session.proxies = {"http": proxy_url, "https": proxy_url}

    # 1) Login
    login_payload = {
        "name": username,
        "password": password,
        "login": "Login"
    }
    resp = session.post(f"{server_url}/login.php", data=login_payload)
    if resp.status_code != 200 or "login" in resp.url.lower():
        raise Exception("Travian Login failed")

    # 2) Farm‑Listen abrufen
    ajax_resp = session.get(f"{server_url}/ajax.php?cmd=getFarmLists")
    ajax_resp.raise_for_status()

    data = ajax_resp.json()
    return data  # erwartet List[{"id":..., "name":..., "farms":[...]}]
