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


class TestConduit(object):
    username = 'valami'
    email = 'valami@gmail.com'
    password = 'Valami01@'

    def setup_method(self):
        s = Service(executable_path=ChromeDriverManager().install())
        o = Options()
        o.add_experimental_option("detach", True)

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

    # def generate_random_username(length=10):
    #     return ''.join(random.choices(string.ascii_lowercase, k=length))
    #
    # def generate_random_email():
    #     username = generate_random_username()
    #     return f"{username}@gmail.com"
    #
    # def generate_random_password(length=10):
    #     chars = string.ascii_letters + '@' + string.digits
    #     password = ''.join(random.choices(chars, k=length))
    #     return password

    # def test_registration(browser):
    #     # Navigate to registration page
    #     browser.get("http://localhost:1667/#/register")
    #
    #     # Generate random username, email, and password
    #     username = generate_random_username()
    #     email = generate_random_email()
    #     password = generate_random_password()
    #
    #     # Fill in registration form
    #     username_input = WebDriverWait(browser, 5).until(
    #         EC.presence_of_element_located((By.XPATH, '//input[@placeholder="Username"]')))
    #     email_input = browser.find_element(By.XPATH, '//input[@placeholder="Email"]')
    #     password_input = browser.find_element(By.XPATH, '//input[@placeholder="Password"]')
    #     submit_button = browser.find_element(By.XPATH, '//button[@type="submit"]')
    #
    #     username_input.send_keys(username)
    #     email_input.send_keys(email)
    #     password_input.send_keys(password)
    #     submit_button.click()
    #
    #     # Verify that user is logged in
    #     nav_links = WebDriverWait(browser, 5).until(
    #         EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'a[class="nav-link"]')))
    #     assert nav_links[2].text == username


#TC3 - Bejelentkezés

    def test_login(self):
        signin_button = self.browser.find_element(By.XPATH, '//a[@href="#/login"]')
        signin_button.click()

        email_input = self.browser.find_element(By.XPATH, '//input[@placeholder="Email"]')
        password_input = self.browser.find_element(By.XPATH, '//input[@placeholder="Password"]')
        confirm_signin = self.browser.find_element(By.XPATH, '//button[@class="btn btn-lg btn-primary pull-xs-right"]')

        email_input.send_keys(self.email)
        password_input.send_keys(self.password)
        confirm_signin.click()
        time.sleep(1)

        nav_links = WebDriverWait(self.browser, 5).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'a[class="nav-link"]')))
        time.sleep(1)
        profile = nav_links[2]
        assert profile.text == self.username
