# bot/travian_bot.py
import time
import random
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

def login_and_save_session(username: str, password: str, server_url: str, proxy: dict):
    """
    (Optional) Here you could persist cookies or token.
    We just keep credentials in memory in main.py.
    """
    return

def get_farm_lists(username: str, password: str, server_url: str, proxy: dict) -> list:
    """
    Launch a headless Chrome, log in, navigate to the farm list page
    and scrape the farm names. Returns a list of strings.
    """
    chrome_opts = Options()
    chrome_opts.add_argument("--headless")
    chrome_opts.add_argument("--disable-dev-shm-usage")
    chrome_opts.add_argument("--no-sandbox")
    # apply proxy if provided
    if proxy.get("ip") and proxy.get("port"):
        proxy_str = f"{proxy['ip']}:{proxy['port']}"
        chrome_opts.add_argument(f"--proxy-server=http://{proxy_str}")

    driver = webdriver.Chrome(ChromeDriverManager().install(), options=chrome_opts)
    try:
        # 1) Go to login page
        driver.get(f"{server_url}/login.php")
        time.sleep(2)

        # 2) Fill in credentials
        driver.find_element(By.NAME, "name").send_keys(username)
        driver.find_element(By.NAME, "password").send_keys(password)
        driver.find_element(By.XPATH, "//button[@type='submit']").click()
        time.sleep(5)

        # 3) Navigate to farm‑list page (ID may vary; default Travian Legends = 39)
        driver.get(f"{server_url}/build.php?id=39")
        time.sleep(2)

        # 4) Scrape farm‐list entries
        elements = driver.find_elements(By.CLASS_NAME, "raidListSlotTitle")
        farms = [el.text.strip() for el in elements if el.text.strip()]
        return farms

    finally:
        driver.quit()

def run_farming_bot(
    username: str,
    password: str,
    server_url: str,
    proxy: dict,
    interval_min: int,
    interval_max: int,
    random_delay: bool
):
    """
    Simple infinite loop: every interval attack all farms.
    Here we just log to console; you can expand with real raid logic.
    """
    while True:
        print(f"[Bot] Running raid cycle for {username} …")
        # TODO: implement actual raid logic here
        # e.g. call get_farm_lists and then send raids

        wait_minutes = random.randint(interval_min, interval_max)
        wait_seconds = wait_minutes * 60
        if random_delay:
            wait_seconds += random.randint(0, 30)
        print(f"[Bot] Next raid in {wait_seconds} seconds")
        time.sleep(wait_seconds)
