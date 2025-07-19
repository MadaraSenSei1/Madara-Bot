# bot/travian_bot.py
import os, time, random
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

# Env‑Variablen für Chrome/Chromedriver
CHROME_BIN = os.getenv("GOOGLE_CHROME_SHIM", "/usr/bin/google-chrome")
CHROMEDRIVER = os.getenv("CHROMEDRIVER_PATH", "/usr/local/bin/chromedriver")

def _make_driver(proxy_ip=None, proxy_port=None, proxy_user=None, proxy_pass=None):
    opts = Options()
    opts.headless = True
    opts.binary_location = CHROME_BIN
    opts.add_argument("--no-sandbox")
    opts.add_argument("--disable-dev-shm-usage")
    if proxy_ip and proxy_port:
        auth = ""
        if proxy_user and proxy_pass:
            auth = f"{proxy_user}:{proxy_pass}@"
        opts.add_argument(f"--proxy-server=http://{auth}{proxy_ip}:{proxy_port}")
    driver = webdriver.Chrome(executable_path=CHROMEDRIVER, options=opts)
    return driver

def login_and_fetch_farms(username, password, server_url,
                          proxy_ip=None, proxy_port=None,
                          proxy_user=None, proxy_pass=None):
    """
    Loggt sich ein und liefert eine Liste aller Farm‑Targets:
      [{"id":..., "name":..., "coords":"x|y"}, ...]
    """
    driver = _make_driver(proxy_ip, proxy_port, proxy_user, proxy_pass)
    driver.get(server_url + "/login.php")
    time.sleep(2)

    # **Anpassen** falls die Travian‑Login‑Form anders heißt
    driver.find_element(By.NAME, "name").send_keys(username)
    driver.find_element(By.NAME, "password").send_keys(password)
    driver.find_element(By.XPATH, "//button[@type='submit']").click()
    time.sleep(3)

    # Prüfen ob login erfolgreich
    if "login" in driver.current_url.lower() or "fehler" in driver.page_source.lower():
        driver.quit()
        raise Exception("Travian login failed")

    # Beispiel: Scrape Farm‑Liste (anpassen an das Travian‑DOM)
    farms = []
    for elem in driver.find_elements(By.CSS_SELECTOR, ".farmListRow"):
        fid = elem.get_attribute("data-id")
        name = elem.find_element(By.CSS_SELECTOR, ".farmName").text
        coords= elem.find_element(By.CSS_SELECTOR, ".coords").text
        farms.append({"id": fid, "name": name, "coords": coords})

    driver.quit()
    return farms

def raid_one_farm(farm, server_url, proxy_ip=None, proxy_port=None,
                  proxy_user=None, proxy_pass=None):
    """
    Führt genau eine Raid‑Aktion auf 'farm' aus.
    Hier müsst ihr reinkodieren, wie Travian das auslöst.
    """
    # Stub: Im echten Code wieder neuen Driver öffnen,
    # ins Dorf einsteigen und Angriff schicken!
    time.sleep(1)
    return {"farmId": farm["id"], "result": "ok"}
