from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.common.exceptions import WebDriverException
import time

def get_farm_lists(username, password, server_url, proxy_ip, proxy_port, proxy_user, proxy_pass):
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--no-sandbox")

    if proxy_ip and proxy_port and proxy_user and proxy_pass:
        proxy = f"http://{proxy_user}:{proxy_pass}@{proxy_ip}:{proxy_port}"
        chrome_options.add_argument(f"--proxy-server={proxy}")

    try:
        driver = webdriver.Chrome(options=chrome_options)
        driver.get(server_url)
        time.sleep(3)

        driver.find_element(By.NAME, "name").send_keys(username)
        driver.find_element(By.NAME, "password").send_keys(password)
        driver.find_element(By.XPATH, '//button[@type="submit"]').click()
        time.sleep(5)

        if "login" in driver.current_url or "fehler" in driver.page_source.lower():
            raise Exception("Login fehlgeschlagen")

        # Dummy-Liste zur Demonstration
        farm_lists = [{"id": 1, "name": "Farm Nord"}, {"id": 2, "name": "Farm Süd"}]
        driver.quit()
        return farm_lists

    except WebDriverException as e:
        raise Exception(f"Selenium Fehler: {e}")
