# bot/travian_bot.py
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time
import random

class TravianBot:
    def __init__(self, username, password, server_url, proxy=None):
        self.username = username
        self.password = password
        self.server_url = server_url
        self.proxy = proxy
        self.driver = None

    def _get_driver(self):
        chrome_options = Options()
        chrome_options.add_argument("--headless=new")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--no-sandbox")

        if self.proxy:
            proxy_url = f"{self.proxy['ip']}:{self.proxy['port']}"
            if self.proxy.get("username") and self.proxy.get("password"):
                # Für Proxies mit Authentifizierung wäre ein Proxy-Plugin oder -Manager nötig.
                print("⚠️ Authentifizierter Proxy wird verwendet (bitte erweitern für echten Support)")
            chrome_options.add_argument(f"--proxy-server=http://{proxy_url}")

        return webdriver.Chrome(options=chrome_options)

    def login(self):
        try:
            self.driver = self._get_driver()
            self.driver.get(self.server_url)

            time.sleep(2)
            self.driver.find_element(By.NAME, "name").send_keys(self.username)
            self.driver.find_element(By.NAME, "password").send_keys(self.password)
            self.driver.find_element(By.XPATH, "//button[@type='submit']").click()
            time.sleep(4)

            # Erfolg prüfen: Gibt es ein Logout-Menü?
            if "dorf1.php" in self.driver.current_url or "dorf2.php" in self.driver.current_url:
                return True
            return False
        except Exception as e:
            print("Login error:", e)
            return False

    def get_farm_lists(self):
        try:
            self.driver.get(f"{self.server_url}/build.php?tt=99")  # Farm-Listen-Seite
            time.sleep(3)

            farm_list_elements = self.driver.find_elements(By.CLASS_NAME, "listEntry")
            farm_lists = []

            for element in farm_list_elements:
                name_el = element.find_element(By.CLASS_NAME, "listName")
                farm_lists.append(name_el.text.strip())

            return farm_lists
        except Exception as e:
            print("Farm list fetch error:", e)
            return []

    def send_farms(self):
        try:
            self.driver.get(f"{self.server_url}/build.php?tt=99")  # Farm-Listen-Seite
            time.sleep(3)

            checkboxes = self.driver.find_elements(By.XPATH, "//input[@type='checkbox' and contains(@name, 'list')]")
            for checkbox in checkboxes:
                if not checkbox.is_selected():
                    checkbox.click()

            submit_button = self.driver.find_element(By.XPATH, "//button[contains(@class,'startRaid')]")
            submit_button.click()
            print("✅ Farm-Listen gestartet")
            time.sleep(2)
        except Exception as e:
            print("Farm senden fehlgeschlagen:", e)

    def random_float(self):
        return random.uniform(0.0, 1.0)

    def random_offset(self):
        return random.randint(-30, 30)  # Sekunden
