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

    username = 'james_bond'
    email = 'james_bond007@gmail.com'
    password = 'James007'


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

        print("TC1 - Az adatkezelési nyilatkozat használata teszteset sikeresen lefutott!")
    #
    # TC2 - Regisztráció

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
        time.sleep(2)
        assert self.browser.find_element(By.XPATH, '//button[@class="swal-button swal-button--confirm"]').is_displayed()
        reg_ok_button = self.browser.find_element(By.XPATH, '//button[text()="OK"]')
        time.sleep(2)
        reg_ok_button.click()

        print("TC2 - A regisztráció teszteset sikeresen lefutott!")

    # TC3 - Bejelentkezés

    def test_login(self):
        self.login()

        nav_links = WebDriverWait(self.browser, 5).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'a[class="nav-link"]')))
        profile = nav_links[2]
        assert profile.text == self.username
        print("TC3 - A bejelentkezés teszteset sikeresen lefutott!")

    # TC4 - Adatok listázása
    def test_data_list(self):
        self.login()
        time.sleep(2)

        # Global Feed
        global_feed_link = self.browser.find_element(By.XPATH, '//a[@href="#/" and @aria-current="page"]')
        global_feed_link.click()
        time.sleep(2)
        articles = self.browser.find_elements(By.XPATH,
                                              '//div[contains(@class, "home-page")]//div[contains(@class, "article-preview")]//h1')
        article_titles = [article.text for article in articles[:10]]

        print("\nA global feed első 10 bejegyzése:")
        for i, title in enumerate(article_titles, start=1):
            print(f"{i}. {title}")

        time.sleep(2)

        self.browser.refresh()
        time.sleep(2)

        refreshed_articles = self.browser.find_elements(By.XPATH,
                                                    '//div[contains(@class, "home-page")]//div[contains(@class, "article-preview")]//h1')

        refreshed_article_titles = [article.text for article in refreshed_articles[:10]]
        assert article_titles == refreshed_article_titles
        print("TC4 - Adatok listázása teszteset sikeresen lefutott!")

    # TC5 - Több oldalas lista bejárása

    def test_all_pages(self):
        self.login()
        time.sleep(2)
        page_numbers = self.browser.find_elements(By.XPATH, '//a[@class="page-link"]')
        pages = []
        for link in page_numbers:
            link.click()
            pages.append(link)
        time.sleep(2)
        assert len(page_numbers) == len(pages)
        print("TC5 - A több oldalas lista bejárása teszteset sikeresen lefutott!")

    # TC6 - Új adat bevitel
    def test_new_article(self):
        self.login()
        time.sleep(2)
        new_article_button = self.browser.find_element(By.XPATH, '//a[@href="#/editor"]')
        new_article_button.click()
        time.sleep(1)
        title_input = WebDriverWait(self.browser, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'input[placeholder="Article Title"]')))
        title_input.send_keys("Új adat bevitel teszt title")

        about_input = self.browser.find_element(By.CSS_SELECTOR, 'input[placeholder="What\'s this article about?"]')
        about_input.send_keys("Új adat bevitel teszt about")

        article_input = self.browser.find_element(By.CSS_SELECTOR,
                                                  'textarea[placeholder="Write your article (in markdown)"]')
        article_input.send_keys("Új adat bevitel teszt article")

        tag_input = self.browser.find_element(By.CSS_SELECTOR, 'input[placeholder="Enter tags"]')
        tag_input.send_keys("Új adat bevitel teszt tag")

        publish_button = self.browser.find_element(By.XPATH, '//button[contains(text(),"Publish Article")]')
        publish_button.click()
        time.sleep(2)

        title_elements = self.browser.find_elements(By.CSS_SELECTOR, 'h1')
        assert any(title.text == 'Új adat bevitel teszt title' for title in title_elements)
        print("TC6 - Az új adat bevitel teszteset sikeresen lefutott!")

    #TC7 Ismételt és sorozatos adatbevitel adatforrásból

    # def test_import_datas_from_csv(self):
    #     self.login()
    #     time.sleep(2)
    #     with open('datas.csv', 'r') as file:
    #         reader = csv.reader(file)
    #         next(reader)
    #         for row in reader:
    #             title, about, article, tag = row
    #
    #             new_article_button = self.browser.find_element(By.XPATH, '//a[@href="#/editor"]')
    #             new_article_button.click()
    #
    #             WebDriverWait(self.browser, 10).until(
    #                 EC.presence_of_element_located((By.XPATH, '//input[@placeholder="Article Title"]'))
    #             )
    #
    #             title_input = self.browser.find_element(By.XPATH, '//input[@placeholder="Article Title"]')
    #             title_input.send_keys(title)
    #
    #             about_input = self.browser.find_element(By.XPATH, '//input[@placeholder="What\'s this article about?"]')
    #             about_input.send_keys(about)
    #
    #             article_input = self.browser.find_element(By.XPATH,
    #                                                       '//textarea[@placeholder="Write your article (in markdown)"]')
    #             article_input.send_keys(article)
    #
    #             tag_input = self.browser.find_element(By.XPATH, '//input[@placeholder="Enter tags"]')
    #             tag_input.send_keys(tag)
    #             tag_input.send_keys(Keys.RETURN)
    #
    #             publish_button = self.browser.find_element(By.XPATH, '//button[contains(text(), "Publish Article")]')
    #             publish_button.click()
    #
    #             article_title = WebDriverWait(self.browser, 10).until(
    #                 EC.presence_of_element_located((By.XPATH, '//h1'))
    #             )
    #
    #             assert article_title.text == title
    #             print("TC7 - Az ismételt és sorozatos adatbevitel adatforrásból teszteset sikeresen lefutott!")

#     # TC8 Meglévő adat módosítás

    def test_modification_of_existing_username(self):
        self.login()
        time.sleep(2)
        settings_link = self.browser.find_element(By.XPATH, '//a[@href="#/settings"]')
        settings_link.click()
        time.sleep(1)
        current_username_input = self.browser.find_element(By.XPATH, '//input[@placeholder="Your username"]')
        current_username = current_username_input.get_attribute('value')
        current_username_input.clear()
        modified_username = current_username + " módosítva"
        for char in modified_username:
            current_username_input.send_keys(char)
            time.sleep(0.1)
        update_settings_button = self.browser.find_element(By.XPATH, '//button[contains(text(), "Update Settings")]')
        update_settings_button.click()
        updated_username = self.browser.find_element(By.XPATH, '//input[@placeholder="Your username"]') \
            .get_attribute('value')
        assert updated_username == modified_username
        print("TC8 - A meglévő adat módosítás teszteset sikeresen lefutott!")
#
#     # TC9 Adat vagy adatok törlése.

    def test_delete_data(self):
        self.login()

        time.sleep(2)

        new_article_link = self.browser.find_element(By.XPATH, '//a[contains(text(), "New Article")]')
        new_article_link.click()
        time.sleep(1)

        title_input = self.browser.find_element(By.XPATH, '//input[@placeholder="Article Title"]')
        title_input.send_keys("Rövid életű title")

        description_input = self.browser.find_element(By.XPATH, '//input[@placeholder="What\'s this article about?"]')
        description_input.send_keys("Rövid életű description")

        body_input = self.browser.find_element(By.XPATH, '//textarea[@placeholder="Write your article (in markdown)"]')
        body_input.send_keys("Rövid életű body")

        tags_input = self.browser.find_element(By.XPATH, '//input[@placeholder="Enter tags"]')
        tags_input.send_keys("Rövid életű tags")

        publish_button = self.browser.find_element(By.XPATH, '//button[contains(text(), "Publish Article")]')
        publish_button.click()
        time.sleep(1)

        comment_button = self.browser.find_element(By.XPATH, '//button[contains(text(), "Post Comment")]')
        comment_textarea = self.browser.find_element(By.XPATH, "//textarea[@placeholder='Write a comment...']")
        comment_textarea.send_keys("Rövid életű komment")
        comment_button.click()
        time.sleep(2)
        comment_element = self.browser.find_element(By.XPATH, '//p[@class="card-text"]')
        assert comment_element.text == "Rövid életű komment"

        time.sleep(1)

        trash_icon = self.browser.find_element(By.XPATH, '//i[@class="ion-trash-a"]')
        trash_icon.click()

        assert comment_element is not None
        print("TC9 - Adat vagy adatok törlése teszteset sikeresen lefutott!")
#
# # TC10 Adatok lementése a felületről

    # def test_save_data_to_csv(self):
    #     self.login()
    #     time.sleep(2)
    #     tag_list = WebDriverWait(self.browser, 5).until(EC.presence_of_all_elements_located(
    #         (By.XPATH, '//div[@class="sidebar"]/div/a[@class="tag-pill tag-default"]')))
    #     with open('tags.csv', 'w') as file:
    #         writer = csv.writer(file)
    #         for tag in tag_list:
    #             writer.writerow([tag.text])
    #     with open('tags.csv', 'r') as file:
    #         first_row = file.readline().rstrip('\n')
    #         assert first_row == tag_list[0].text
    #         print("TC4 - Az adatok listázása teszteset sikeresen lefutott!")
#
#     # TC11 Kijelentkezés
#
    def test_logout(self):
        self.login()
        time.sleep(2)

        logout_button = self.browser.find_element(By.XPATH, '//a[contains(.,"Log out")]')
        logout_button.click()

        login_link = self.browser.find_element(By.CSS_SELECTOR, 'a[href="#/login"]')
        assert login_link.is_displayed(), "Login link is not displayed"
        print("TC11 - A kijelentkezés teszteset sikeresen lefutott!")
#
