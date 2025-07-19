# bot/travian_bot.py

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time

def login_and_get_farms(username, password, server_url,
                        proxy_ip=None, proxy_port=None, proxy_user=None, proxy_pass=None):
    opts = Options()
    opts.add_argument("--headless")
    opts.add_argument("--no-sandbox")
    # Proxy‐Setup falls gesetzt
    if proxy_ip and proxy_port:
        proxy = f"{proxy_ip}:{proxy_port}"
        if proxy_user and proxy_pass:
            proxy = f"{proxy_user}:{proxy_pass}@{proxy}"
        opts.add_argument(f"--proxy-server=http://{proxy}")

    driver = webdriver.Chrome(options=opts)
    try:
        driver.get(server_url)
        time.sleep(2)
        # Hier die korrekten Locators für Travian eintragen:
        driver.find_element(By.NAME, "name").send_keys(username)
        driver.find_element(By.NAME, "password").send_keys(password)
        driver.find_element(By.XPATH, "//button[@type='submit']").click()
        time.sleep(3)

        # Beispiel: Farm‑Items auslesen (XPath/Selector anpassen!)
        farms = []
        elements = driver.find_elements(By.CSS_SELECTOR, ".farmListItem")
        for el in elements:
            farms.append(el.text)
        return farms

    finally:
        driver.quit()
