import time
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
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

    #TC1 - Regisztráció

    #TC2 - Bejelentkezés

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

        nav_links = WebDriverWait(self.browser, 5).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'a[class="nav-link"]')))
        time.sleep(1)
        profile = nav_links[2]
        assert profile.text == self.username

    #TC3 - Adatkezelési nyilatkozat használata

    #TC4 - Adatok listázása


    #TC5 - Több oldalas lista bejárása

    def test_all_pages(self):

        signin_button = self.browser.find_element(By.XPATH, '//a[@href="#/login"]')
        signin_button.click()

        email_input = self.browser.find_element(By.XPATH, '//input[@placeholder="Email"]')
        password_input = self.browser.find_element(By.XPATH, '//input[@placeholder="Password"]')
        confirm_signin = self.browser.find_element(By.XPATH, '//button[@class="btn btn-lg btn-primary pull-xs-right"]')

        email_input.send_keys(self.email)
        password_input.send_keys(self.password)
        confirm_signin.click()
        time.sleep(1)

        page_numbers = self.browser.find_elements(By.XPATH, '//a[@class="page-link"]')

        pages = []
        for link in page_numbers:
            link.click()
            pages.append(link)

        assert len(page_numbers) == len(pages)


    #TC6 - Új adat bevitel


    #TC7 Ismételt és sorozatos adatbevitel adatforrásból

    #TC11 Kijelentkezés

    def test_logout(self):
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

        logout_button = self.browser.find_element(By.XPATH, '//a[contains(.,"Log out")]')
        logout_button.click()




