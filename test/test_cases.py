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
        #self.browser.quit()

# TC1 - Adatkezelési nyilatkozat használata

    def test_cookies(self):
        decline_btn = self.browser.find_element(By.XPATH,
                                                "//button[@class= 'cookie__bar__buttons__button cookie__bar__buttons__button--decline']")
        decline_btn.click()

        cookie_decline = self.browser.get_cookie("vue-cookie-accept-decline-cookie-policy-panel")

        assert cookie_decline["value"] == "decline"

        self.browser.delete_cookie("vue-cookie-accept-decline-cookie-policy-panel")
        self.browser.refresh()

        accept_btn = WebDriverWait(self.browser, 5).until(EC.presence_of_element_located(
            (By.XPATH, "//button[@class= 'cookie__bar__buttons__button cookie__bar__buttons__button--accept']")))
        accept_btn.click()

        cookie_accept = self.browser.get_cookie("vue-cookie-accept-decline-cookie-policy-panel")

        assert cookie_accept["value"] == "accept"
        time.sleep(2)

    #TC2 - Regisztráció

    def test_registration(self):
        signup_button = self.browser.find_element(By.XPATH, '//a[@href="#/register"]')
        signup_button.click()

        username_input = self.browser.find_element(By.XPATH, '//input[@placeholder="Username"]')
        email_input = self.browser.find_element(By.XPATH, '//input[@placeholder="Email"]')
        password_input = self.browser.find_element(By.XPATH, '//input[@placeholder="Password"]')
        signup_button = self.browser.find_element(By.XPATH, '//button[@class="btn btn-lg btn-primary pull-xs-right"]')

        username_input.send_keys(self.username)
        email_input.send_keys(self.email)
        password_input.send_keys(self.password)
        signup_button.click()
        time.sleep(5)
        nav_links = WebDriverWait(self.browser, 5).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'a[class="nav-link"]')))
        time.sleep(5)
        profile = nav_links[2]
        assert profile.text == self.username
