# bot/travian_bot.py

import time
import random
import threading
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.proxy import Proxy, ProxyType
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

class TravianBot:
    def __init__(self, account_id, username, password, server_url, min_interval, max_interval, add_random, proxy_data=None):
        self.account_id = account_id
        self.username = username
        self.password = password
        self.server_url = server_url
        self.min_interval = min_interval
        self.max_interval = max_interval
        self.add_random = add_random
        self.proxy_data = proxy_data
        self.driver = None
        self.running = False
        self.thread = None
        self.farm_lists = []

    def _init_driver(self):
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--window-size=1920x1080")

        if self.proxy_data:
            proxy_str = f"{self.proxy_data['ip']}:{self.proxy_data['port']}"
            if self.proxy_data.get("username") and self.proxy_data.get("password"):
                proxy_str = f"{self.proxy_data['username']}:{self.proxy_data['password']}@{proxy_str}"
            chrome_options.add_argument(f'--proxy-server=http://{proxy_str}')

        service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service, options=chrome_options)

    def login(self):
        self._init_driver()
        self.driver.get(self.server_url)

        try:
            self.driver.find_element(By.NAME, "name").send_keys(self.username)
            self.driver.find_element(By.NAME, "password").send_keys(self.password)
            self.driver.find_element(By.XPATH, "//button[@type='submit']").click()
            time.sleep(3)

            # Check successful login
            if "dorf1.php" in self.driver.current_url:
                return True
            return False
        except Exception as e:
            print(f"[LOGIN ERROR] {e}")
            return False

    def get_farm_lists(self):
        try:
            self.driver.get(f"{self.server_url}/build.php?id=39&gid=16")
            time.sleep(3)

            lists = self.driver.find_elements(By.XPATH, "//div[contains(@class, 'farmList')]//button[contains(@name, 'a')]")
            self.farm_lists = [btn.get_attribute("name") for btn in lists if btn.get_attribute("name")]
            return self.farm_lists
        except Exception as e:
            print(f"[FARMLIST ERROR] {e}")
            return []

    def start(self):
        if not self.running:
            self.running = True
            self.thread = threading.Thread(target=self._run_loop)
            self.thread.start()

    def stop(self):
        self.running = False
        if self.thread and self.thread.is_alive():
            self.thread.join()
        if self.driver:
            self.driver.quit()

    def _run_loop(self):
        while self.running:
            try:
                for farm in self.farm_lists:
                    self.driver.get(f"{self.server_url}/build.php?id=39&gid=16")
                    time.sleep(1)
                    try:
                        raid_button = self.driver.find_element(By.NAME, farm)
                        raid_button.click()
                        print(f"[RAID] Sent raid with {farm}")
                    except Exception as e:
                        print(f"[RAID ERROR] {e}")
                    time.sleep(2)

                wait_time = random.randint(self.min_interval, self.max_interval)
                if self.add_random:
                    wait_time += random.randint(0, 30)
                print(f"[WAIT] Next loop in {wait_time} seconds")
                time.sleep(wait_time)
            except Exception as e:
                print(f"[LOOP ERROR] {e}")
                self.running = False
