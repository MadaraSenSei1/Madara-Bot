from selenium import webdriver
from selenium.webdriver.common.by import By
import time

def get_farm_lists(username, password, server_url, proxy_ip, proxy_port, proxy_user, proxy_pass):
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")

    if proxy_ip and proxy_port:
        proxy = f"{proxy_ip}:{proxy_port}"
        chrome_options.add_argument(f'--proxy-server=http://{proxy}')

    driver = webdriver.Chrome(options=chrome_options)

    try:
        driver.get(server_url)
        time.sleep(2)

        driver.find_element(By.NAME, "name").send_keys(username)
        driver.find_element(By.NAME, "password").send_keys(password)
        driver.find_element(By.XPATH, "//button[@type='submit']").click()
        time.sleep(3)

        # Beispielhafte Farm-Listen-Auslesung (anpassen je nach Travian-Version)
        driver.get(f"{server_url}/build.php?tt=99")
        time.sleep(2)
        farm_list_elements = driver.find_elements(By.CLASS_NAME, "listTitle")

        farm_names = [elem.text for elem in farm_list_elements]
        return farm_names
    finally:
        driver.quit()
