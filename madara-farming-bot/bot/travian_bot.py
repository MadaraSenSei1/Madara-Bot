import time
import random
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

def get_farm_lists(username, password, server_url, proxy_ip="", proxy_port="", proxy_user="", proxy_pass=""):
    # Setup Selenium with proxy (if provided)
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    if proxy_ip and proxy_port:
    if proxy_user and proxy_pass:
        chrome_options.add_argument(f'--proxy-server=http://{proxy_user}:{proxy_pass}@{proxy_ip}:{proxy_port}')
    else:
        chrome_options.add_argument(f'--proxy-server=http://{proxy_ip}:{proxy_port}')

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

    try:
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

        return farm_lists

    except Exception as e:
        raise Exception(f"Travian error: {str(e)}")

    finally:
        driver.quit()


def run_bot(
    username: str,
    password: str,
    server_url: str,
    proxy_ip: str,
    proxy_port: str,
    proxy_user: str,
    proxy_pass: str,
    interval_min: int,
    interval_max: int,
    randomize: bool
):
    """Background loop: placeholder for actual raid logic."""
    while True:
        wait_seconds = random.randint(interval_min * 60, interval_max * 60)
        if randomize:
            wait_seconds += random.randint(0, 30)
        print(f"[{username}] Waiting {wait_seconds} seconds before next cycle")
        time.sleep(wait_seconds)
        # TODO: Add actual farming/raiding logic here
