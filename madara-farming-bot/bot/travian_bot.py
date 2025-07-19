import time
import random
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

def get_farm_lists(username, password, server_url, proxy_ip="", proxy_port="", proxy_user="", proxy_pass=""):
    try:
        # Setup Selenium with proxy (if provided)
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")

        if proxy_ip and proxy_port:
            proxy_auth = f"{proxy_user}:{proxy_pass}@" if proxy_user and proxy_pass else ""
            chrome_options.add_argument(f'--proxy-server=http://{proxy_auth}{proxy_ip}:{proxy_port}')

        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

        # Login to Travian
        driver.get(server_url)
        time.sleep(2)

        driver.find_element(By.NAME, "name").send_keys(username)
        driver.find_element(By.NAME, "password").send_keys(password)
        driver.find_element(By.XPATH, '//button[@type="submit"]').click()
        time.sleep(5)

        # Navigate to farm list page
        driver.get(f"{server_url}/build.php?tt=99")
        time.sleep(3)

        farm_lists = []
        list_elements = driver.find_elements(By.CLASS_NAME, "raidList")

        for el in list_elements:
            name = el.find_element(By.CLASS_NAME, "listTitleText").text
            farm_lists.append(name)

        driver.quit()
        return farm_lists

    except Exception as e:
        driver.quit()
        raise Exception(f"Travian error: {str(e)}")


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
