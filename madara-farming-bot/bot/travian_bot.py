
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import threading
import time
import random

# Login und Session speichern
def login_and_save_session(username, password, server_url, proxy):
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--no-sandbox")

    if proxy["ip"] and proxy["port"]:
        proxy_str = f"{proxy['ip']}:{proxy['port']}"
        chrome_options.add_argument(f'--proxy-server=http://{proxy_str}')

    driver = webdriver.Chrome(options=chrome_options)
    driver.get(server_url)
    time.sleep(2)
    driver.find_element(By.LINK_TEXT, "Login").click()
    time.sleep(2)
    driver.find_element(By.NAME, "name").send_keys(username)
    driver.find_element(By.NAME, "password").send_keys(password)
    driver.find_element(By.XPATH, "//button[@type='submit']").click()
    time.sleep(5)
    return {
        "driver": driver,
        "url": server_url
    }

# Farmlisten scrapen
def get_farm_lists(session):
    driver = session["driver"]
    driver.get(f"{session['url']}/build.php?id=39")
    time.sleep(3)
    elements = driver.find_elements(By.CLASS_NAME, "raidListSlotTitle")
    return [el.text for el in elements if el.text.strip()]

# Bot starten
def start_farming_bot(session, interval_min, interval_max):
    def loop_raids():
        while True:
            try:
                driver = session["driver"]
                driver.get(f"{session['url']}/build.php?id=39")
                time.sleep(3)
                send_buttons = driver.find_elements(By.CSS_SELECTOR, "button[type='submit']")
                for btn in send_buttons:
                    try:
                        btn.click()
                        time.sleep(1)
                    except:
                        continue
                delay = random.randint(interval_min * 60, interval_max * 60) + random.randint(0, 30)
                print(f"Next raid in {delay} seconds")
                time.sleep(delay)
            except Exception as e:
                print("Error in bot loop:", e)
                break

    thread = threading.Thread(target=loop_raids)
    thread.start()
