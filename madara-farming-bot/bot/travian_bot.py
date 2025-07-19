import time
import random
import asyncio
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

def create_driver(proxy):
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--no-sandbox")

    if proxy["ip"] and proxy["port"]:
        proxy_auth = ""
        if proxy["username"] and proxy["password"]:
            proxy_auth = f"{proxy['username']}:{proxy['password']}@"
        chrome_options.add_argument(
            f'--proxy-server=http://{proxy_auth}{proxy["ip"]}:{proxy["port"]}'
        )

    return webdriver.Chrome(options=chrome_options)

def login_and_get_farms(username, password, server_url, proxy):
    driver = create_driver(proxy)

    try:
        driver.get("https://www.travian.com/international")
        time.sleep(2)
        driver.find_element(By.LINK_TEXT, "Login").click()
        time.sleep(2)

        driver.find_element(By.NAME, "name").send_keys(username)
        driver.find_element(By.NAME, "password").send_keys(password)
        driver.find_element(By.XPATH, "//button[@type='submit']").click()
        time.sleep(5)

        # Gehe zur Farm-List-Seite
        driver.get(f"{server_url}/build.php?id=39&gid=16")
        time.sleep(3)

        farm_elements = driver.find_elements(By.CLASS_NAME, "raidListSlotTitle")
        farms = [el.text for el in farm_elements if el.text.strip() != ""]

        if not farms:
            raise Exception("No farm lists found.")

        return farms

    finally:
        driver.quit()

async def start_farming_bot(username, password, server_url, proxy, interval_min, interval_max, randomize=True):
    async def farm_cycle():
        driver = create_driver(proxy)
        try:
            driver.get("https://www.travian.com/international")
            time.sleep(2)
            driver.find_element(By.LINK_TEXT, "Login").click()
            time.sleep(2)

            driver.find_element(By.NAME, "name").send_keys(username)
            driver.find_element(By.NAME, "password").send_keys(password)
            driver.find_element(By.XPATH, "//button[@type='submit']").click()
            time.sleep(5)

            # Navigiere zur Farmlistenseite
            driver.get(f"{server_url}/build.php?id=39&gid=16")
            time.sleep(3)

            # Klick auf alle Raid-Buttons
            send_buttons = driver.find_elements(By.XPATH, "//button[contains(@class, 'startRaid')]")
            for btn in send_buttons:
                try:
                    btn.click()
                    time.sleep(1)
                except Exception:
                    continue

        finally:
            driver.quit()

    # Bestimme zufälliges Intervall
    delay_min = interval_min * 60
    delay_max = interval_max * 60
    next_delay = random.randint(delay_min, delay_max)
    if randomize:
        next_delay += random.randint(0, 30)

    asyncio.create_task(wait_and_farm(next_delay, farm_cycle))

    return next_delay

async def wait_and_farm(delay, task_func):
    await asyncio.sleep(delay)
    await asyncio.to_thread(task_func)
