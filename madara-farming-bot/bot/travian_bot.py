from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time


def get_farm_lists(username, password, proxy, server_url):
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    if proxy and proxy["ip"] and proxy["port"]:
        proxy_str = f'{proxy["ip"]}:{proxy["port"]}'
        chrome_options.add_argument(f'--proxy-server=http://{proxy_str}')

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

    try:
        driver.get(server_url)
        time.sleep(2)
        driver.find_element(By.LINK_TEXT, "Login").click()
        time.sleep(2)
        driver.find_element(By.NAME, "name").send_keys(username)
        driver.find_element(By.NAME, "password").send_keys(password)
        driver.find_element(By.XPATH, "//button[@type='submit']").click()
        time.sleep(4)

        # Gehe zur Farmlistenseite
        driver.get(f"{server_url}/build.php?id=39")
        time.sleep(3)

        farm_elements = driver.find_elements(By.CLASS_NAME, "slotRow")
        farm_names = [el.text.split("\n")[0] for el in farm_elements if el.text.strip()]

        return farm_names

    except Exception as e:
        print("Fehler beim Farmabruf:", e)
        return []

    finally:
        driver.quit()


def run_bot(username, password, proxy, interval_min, interval_max, server_url):
    import random

    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    if proxy and proxy["ip"] and proxy["port"]:
        proxy_str = f'{proxy["ip"]}:{proxy["port"]}'
        chrome_options.add_argument(f'--proxy-server=http://{proxy_str}')

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

    try:
        driver.get(server_url)
        time.sleep(2)
        driver.find_element(By.LINK_TEXT, "Login").click()
        time.sleep(2)
        driver.find_element(By.NAME, "name").send_keys(username)
        driver.find_element(By.NAME, "password").send_keys(password)
        driver.find_element(By.XPATH, "//button[@type='submit']").click()
        time.sleep(4)

        while True:
            driver.get(f"{server_url}/build.php?id=39")
            time.sleep(3)

            raid_buttons = driver.find_elements(By.XPATH, "//button[contains(@id, 'startRaid')]")
            for btn in raid_buttons:
                try:
                    btn.click()
                    time.sleep(1)
                except:
                    continue

            wait_time = random.randint(int(interval_min)*60, int(interval_max)*60)
            print(f"Nächster Angriff in {wait_time//60} Minuten")
            time.sleep(wait_time)

    except Exception as e:
        print("Fehler beim Bot:", e)

    finally:
        driver.quit()
