import time
import random
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

def get_farm_lists(
    username: str,
    password: str,
    server_url: str,
    proxy: dict
) -> list:
    """Log in headlessly and scrape the farm‐list names."""
    chrome_opts = Options()
    chrome_opts.add_argument("--headless")
    chrome_opts.add_argument("--no-sandbox")
    if proxy.get("ip") and proxy.get("port"):
        chrome_opts.add_argument(f"--proxy-server=http://{proxy['ip']}:{proxy['port']}")

    driver = webdriver.Chrome(ChromeDriverManager().install(), options=chrome_opts)
    try:
        # 1) Login
        driver.get(f"{server_url}/login.php")
        time.sleep(2)
        driver.find_element(By.NAME, "name").send_keys(username)
        driver.find_element(By.NAME, "password").send_keys(password)
        driver.find_element(By.XPATH, "//button[@type='submit']").click()
        time.sleep(5)

        # 2) Navigate to farm‐list (build page 39)
        driver.get(f"{server_url}/build.php?id=39")
        time.sleep(2)

        # 3) Scrape list titles
        elems = driver.find_elements(By.CLASS_NAME, "raidListSlotTitle")
        return [e.text.strip() for e in elems if e.text.strip()]
    finally:
        driver.quit()

def run_bot(
    username: str,
    password: str,
    server_url: str,
    proxy: dict,
    interval_min: int,
    interval_max: int,
    random_delay: bool
):
    """Background loop: placeholder for actual raid logic."""
    while True:
        print(f"[{username}] Starting raid cycle…")
        # (Here you could fetch the farm list and dispatch attacks…)
        wait_seconds = random.randint(interval_min, interval_max) * 60
        if random_delay:
            wait_seconds += random.randint(0, 30)
        print(f"[{username}] Sleeping {wait_seconds}s before next cycle")
        time.sleep(wait_seconds)
