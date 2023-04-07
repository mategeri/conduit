import time
import csv
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait


class TestConduit:
    username = 'Tester007'
    email = 'tester007@gmail.com'
    password = 'James@Bond007'

    def setup_method(self):
        s = Service(executable_path=ChromeDriverManager().install())
        o = Options()
        o.add_experimental_option("detach", True)
        o.add_argument('--headless')
        o.add_argument('--no-sandbox')
        o.add_argument('--disable-dev-shm-usage')
        self.browser = webdriver.Chrome(service=s, options=o)
        URL = "http://localhost:1667/#/"
        self.browser.get(URL)
        self.browser.maximize_window()

    def teardown_method(self):
        self.browser.quit()

    def login(self):
        signin_button = self.browser.find_element(By.XPATH, '//a[@href="#/login"]')
        signin_button.click()

        email_input = self.browser.find_element(By.XPATH, '//input[@placeholder="Email"]')
        password_input = self.browser.find_element(By.XPATH, '//input[@placeholder="Password"]')
        confirm_signin = self.browser.find_element(By.XPATH, '//button[@class="btn btn-lg btn-primary pull-xs-right"]')

        email_input.send_keys(self.email)
        password_input.send_keys(self.password)
        confirm_signin.click()
        time.sleep(1)

    # TC1 - Adatkezelési nyilatkozat használata

    def test_cookies(self):
        self.browser.refresh()

        accept_btn = WebDriverWait(self.browser, 5).until(EC.presence_of_element_located(
            (By.XPATH, "//button[@class= 'cookie__bar__buttons__button cookie__bar__buttons__button--accept']")))
        accept_btn.click()

        cookie_accept = self.browser.get_cookie("vue-cookie-accept-decline-cookie-policy-panel")

        assert cookie_accept["value"] == "accept"
        time.sleep(2)
