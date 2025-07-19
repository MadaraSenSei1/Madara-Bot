# bot/travian_bot.py
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import time

def get_farm_lists(username, password, server_url, proxy_ip, proxy_port, proxy_user, proxy_pass):
    options = Options()
    options.headless = True
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    if proxy_ip and proxy_port:
        proxy = f"http://{proxy_user}:{proxy_pass}@{proxy_ip}:{proxy_port}"
        options.add_argument(f'--proxy-server={proxy}')

    driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)

    try:
        driver.get(server_url)
        time.sleep(3)

        # Füllt das Login-Formular aus
        driver.find_element(By.NAME, "name").send_keys(username)
        driver.find_element(By.NAME, "password").send_keys(password)
        driver.find_element(By.NAME, "s1").click()
        time.sleep(3)

        # Prüfe auf Fehlermeldung
        if "login" in driver.current_url or "fehler" in driver.page_source.lower():
            raise Exception("Travian Login failed")

        # Dummy-Farm-Liste für Testzwecke
        farm_lists = ["Farm A", "Farm B", "Farm C"]
        return farm_lists

    except Exception as e:
        raise Exception(f"Bot error: {e}")

    finally:
        driver.quit()
