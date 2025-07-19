from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time
import random

def run_bot(username, password, proxy, interval_min, interval_max):
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--no-sandbox')

    # Proxy einfügen, falls vorhanden
    if proxy and proxy["ip"] and proxy["port"]:
        proxy_string = f'{proxy["ip"]}:{proxy["port"]}'
        chrome_options.add_argument(f'--proxy-server=http://{proxy_string}')

    driver = webdriver.Chrome(options=chrome_options)

    try:
        print("🔐 Logge ein →")
        driver.get("https://www.travian.com/international")

        time.sleep(3)
        login_btn = driver.find_element(By.LINK_TEXT, "Login")
        login_btn.click()

        time.sleep(3)
        driver.find_element(By.NAME, "name").send_keys(username)
        driver.find_element(By.NAME, "password").send_keys(password)
        driver.find_element(By.XPATH, "//button[@type='submit']").click()

        time.sleep(5)
        print("✅ Eingeloggt!")

        # Hier später: Farm-Listen Seite aufrufen
        print("📦 Öffne Farm-Listen-Seite (Platzhalter)")
        # Beispiel: driver.get("https://yourserver.travian.com/build.php?id=39")

    except Exception as e:
        print("❌ Fehler beim Einloggen:", e)

    finally:
        driver.quit()
