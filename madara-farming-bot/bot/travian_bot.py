from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time

def get_farm_lists(username, password, server_url, proxy_ip, proxy_port, proxy_user, proxy_pass):
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--no-sandbox')

    if proxy_ip and proxy_port and proxy_user and proxy_pass:
        proxy = f"http://{proxy_user}:{proxy_pass}@{proxy_ip}:{proxy_port}"
        chrome_options.add_argument(f'--proxy-server={proxy}')

    driver = webdriver.Chrome(options=chrome_options)
    driver.get(server_url)
    time.sleep(3)

    # Login-Versuch
    driver.find_element(By.NAME, "name").send_keys(username)
    driver.find_element(By.NAME, "password").send_keys(password)
    driver.find_element(By.XPATH, "//button[@type='submit']").click()
    time.sleep(3)

    # Erfolgsprüfung
    if "login" in driver.current_url or "fehler" in driver.page_source.lower():
        driver.quit()
        raise Exception("Login failed")

    # Dummy response
    farm_lists = ["Farm 1", "Farm 2"]
    driver.quit()
    return farm_lists
