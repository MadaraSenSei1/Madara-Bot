from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time

def create_driver(proxy):
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--no-sandbox")

    if proxy.get("ip") and proxy.get("port"):
        proxy_str = f"{proxy['ip']}:{proxy['port']}"
        chrome_options.add_argument(f'--proxy-server=http://{proxy_str}')

    return webdriver.Chrome(options=chrome_options)

def login_and_fetch_farms(username, password, server_url, proxy):
    driver = create_driver(proxy)
    try:
        driver.get(server_url)
        time.sleep(2)
        driver.find_element(By.LINK_TEXT, "Login").click()
        time.sleep(2)
        driver.find_element(By.NAME, "name").send_keys(username)
        driver.find_element(By.NAME, "password").send_keys(password)
        driver.find_element(By.XPATH, "//button[@type='submit']").click()
        time.sleep(5)

        driver.get(f"{server_url}/build.php?id=39")  # Farmlist page
        time.sleep(3)

        farm_elements = driver.find_elements(By.CLASS_NAME, "raidListSlotTitle")
        farms = [el.text for el in farm_elements if el.text.strip() != ""]
        return farms
    finally:
        driver.quit()

def run_farming_bot(username, password, server_url, proxy):
    driver = create_driver(proxy)
    try:
        driver.get(server_url)
        time.sleep(2)
        driver.find_element(By.LINK_TEXT, "Login").click()
        time.sleep(2)
        driver.find_element(By.NAME, "name").send_keys(username)
        driver.find_element(By.NAME, "password").send_keys(password)
        driver.find_element(By.XPATH, "//button[@type='submit']").click()
        time.sleep(5)

        driver.get(f"{server_url}/build.php?id=39")  # Farmlist page
        time.sleep(3)

        send_buttons = driver.find_elements(By.CLASS_NAME, "startRaid")
        for btn in send_buttons:
            try:
                btn.click()
                time.sleep(1)
            except:
                continue
    finally:
        driver.quit()
