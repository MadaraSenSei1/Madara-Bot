from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from time import sleep
import random

def get_farm_lists(username, password, proxy, server_url):
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    if proxy["ip"] and proxy["port"]:
        proxy_str = f'{proxy["ip"]}:{proxy["port"]}'
        chrome_options.add_argument(f'--proxy-server=http://{proxy_str}')

    driver = webdriver.Chrome(options=chrome_options)

    try:
        print("🌐 Farm-Listen abrufen...")
        driver.get("https://www.travian.com/international")
        sleep(2)
        driver.find_element(By.LINK_TEXT, "Login").click()
        sleep(2)
        driver.find_element(By.NAME, "name").send_keys(username)
        driver.find_element(By.NAME, "password").send_keys(password)
        driver.find_element(By.XPATH, "//button[@type='submit']").click()
        sleep(3)

        driver.get(f"{server_url}/build.php?id=39")
        sleep(3)
        print("✅ Farm-Listen geladen")
        return ["Farm 1", "Farm 2", "Farm 3"]  # Platzhalter für echte Farmnamen

    finally:
        driver.quit()

def run_bot(username, password, proxy, interval_min, interval_max, server_url):
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    if proxy["ip"] and proxy["port"]:
        proxy_str = f'{proxy["ip"]}:{proxy["port"]}'
        chrome_options.add_argument(f'--proxy-server=http://{proxy_str}')

    driver = webdriver.Chrome(options=chrome_options)

    try:
        print("🤖 Bot startet Login...")
        driver.get("https://www.travian.com/international")
        sleep(2)
        driver.find_element(By.LINK_TEXT, "Login").click()
        sleep(2)
        driver.find_element(By.NAME, "name").send_keys(username)
        driver.find_element(By.NAME, "password").send_keys(password)
        driver.find_element(By.XPATH, "//button[@type='submit']").click()
        sleep(3)

        while True:
            print("⚔️  Sende Angriffe...")
            driver.get(f"{server_url}/build.php?id=39")
            sleep(2)

            # Hier kannst du Klicks oder Aktionen ergänzen

            delay = random.randint(interval_min, interval_max)
            print(f"⏳ Nächster Angriff in {delay} Minuten")
            sleep(delay * 60)

    finally:
        driver.quit()
