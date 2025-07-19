from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time
import random


def run_bot(username, password, proxy, interval_min, interval_max, server_url):
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--no-sandbox")

    if proxy["ip"] and proxy["port"]:
        proxy_str = f"{proxy['ip']}:{proxy['port']}"
        chrome_options.add_argument(f'--proxy-server=http://{proxy_str}')

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

        # Farm-List-Seite aufrufen
        driver.get(f"https://{server_url}/build.php?id=39")
        print("📦 Öffne Farm-Listen-Seite")
        time.sleep(3)

        # Später: Farmen angreifen
        print("🚀 Sende Angriffe... (Platzhalter)")

    finally:
        driver.quit()


def get_farm_lists(username, password, proxy, server_url):
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--no-sandbox")

    if proxy["ip"] and proxy["port"]:
        proxy_str = f"{proxy['ip']}:{proxy['port']}"
        chrome_options.add_argument(f'--proxy-server=http://{proxy_str}')

    driver = webdriver.Chrome(options=chrome_options)

    try:
        print("🔐 Farm-List-Abruf startet...")
        driver.get("https://www.travian.com/international")
        time.sleep(2)

        driver.find_element(By.LINK_TEXT, "Login").click()
        time.sleep(2)
        driver.find_element(By.NAME, "name").send_keys(username)
        driver.find_element(By.NAME, "password").send_keys(password)
        driver.find_element(By.XPATH, "//button[@type='submit']").click()
        time.sleep(5)

        # Rufe die Farm-Listen-Seite des angegebenen Servers auf
        driver.get(f"https://{server_url}/build.php?id=39")
        time.sleep(3)

        # Scrape Farm-Listenelemente
        farm_elements = driver.find_elements(By.CLASS_NAME, "raidListSlotTitle")
        farms = [el.text for el in farm_elements if el.text.strip() != ""]

        print(f"🌾 Farm-Listen gefunden: {farms}")
        return farms

    except Exception as e:
        print(f"⚠️ Fehler beim Abrufen der Farm-Listen: {e}")
        return []

    finally:
        driver.quit()
