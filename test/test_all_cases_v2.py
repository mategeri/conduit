## 1. Sign up automatizálása

import allure
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait


class TestSingUp(object):

    def useRegistrationButton(self):
        WebDriverWait(self.browser, 5).until(
            EC.presence_of_element_located((By.XPATH, '//a[@href="#/register"]'))).click()

    def useSignInButton(self):
        WebDriverWait(self.browser, 5).until(EC.presence_of_element_located((By.XPATH, '//a[@href="#/login"]'))).click()


    def gathering_input_fields(self, inp_fields_elements: dict, placeholders_dict: dict):
        placeholders = list(placeholders_dict.keys())
        # placeholders = ["Username", "Email", "Password"]
        print(placeholders)
        print(placeholders[0])
        for field in range(len(placeholders)):
            inp_fields_elements[f'{placeholders[field]}'] = self.browser.find_element(By.XPATH,
                                                                                      f'//input[@placeholder="{placeholders[field]}"]')
        return inp_fields_elements

    def inp_values(self, sub_dict: str):
        inp_dict = {"Pass": {'Username': 'user99',
                             'Email': 'user99@hotmail.com',
                             'Password': 'Userpass1', },
                    "Fail": {'Username': 'user1',
                             'Email': 'user1@hotmail.com',
                             'Password': '', },
                    "While": {'Username': 'user1',
                              'Email': 'user1@hotmail.com',
                              'Password': 'Userpass1', }
                    }

        return inp_dict[sub_dict]

    def send_inputs(self, inpFields_dict, inp_dict_sub):
        # print(inpFields_dict)
        for pairs in inpFields_dict.items():
            inpName = pairs[0]
            inpValue = pairs[1]
            # print(f'key&value: {inpName}={inpValue}')
            send_this_key = inp_dict_sub[inpName]
            inpValue.send_keys(send_this_key)

        WebDriverWait(self.browser, 5).until(
            EC.presence_of_element_located(
                (By.XPATH, '//button[@class="btn btn-lg btn-primary pull-xs-right"]'))).click()

    def popup_text(self, actual_str:dict):
        WebDriverWait(self.browser, 5).until(
            EC.presence_of_element_located((By.XPATH, '//div[@class="swal-title"]')))
        actual_str['reg_succ'] = self.browser.find_element(By.XPATH, '//div[@class="swal-title"]').text
        actual_str['reg_succ_s'] = self.browser.find_element(By.XPATH, '//div[@class="swal-text"]').text
        return actual_str

    def expected_text(self, info: str):

        expected_str = {"Pass": {'Title': 'Welcome!',
                                 'Text': 'Your registration was successful!'},
                        "Fail": {'Title': 'Registration failed!',
                                 'Text': 'Password field required.'},
                        "While": {'Title': 'Registration failed!',
                                 'Text': 'Email already taken.'},
                        }
        return expected_str[info]

    def popup_ok_btn(self):
        WebDriverWait(self.browser, 5).until(
            EC.presence_of_element_located((By.XPATH, '//button[@class="swal-button swal-button--confirm"]'))).click()
    def setup_method(self):
        service = Service(executable_path=ChromeDriverManager().install())
        options = Options()
        options.add_experimental_option("detach", True)
        # options.add_argument('--headless')
        # options.add_argument('--no-sandbox')
        # options.add_argument('--disable-dev-shm-usage')
        options.add_argument('window-position=-1000,0')
        self.browser = webdriver.Chrome(service=service, options=options)
        URL = "http://localhost:1667/"
        self.browser.get(URL)
        self.browser.maximize_window()

        # self.registration_button = self.useRegistrationButton()

    def teardown_method(self):
        # pass
        self.browser.quit()

    @allure.id('TC1.1. N+')
    @allure.title('Regisztrációs kisérlet - jelszó nélkül')
    def test_sign_up_direct_neg(self):
        ### belépési kisérlet jelszó nélkül - direkt negatív ág
        self.useRegistrationButton()

        ### Input értékek kigyűjtése, mezők kitöltése és elküldése
        inp_dict_sub = self.inp_values(sub_dict='Fail')
        print(f'\na Fail értékei:')
        for p in inp_dict_sub.values():
            print(p)

        inpFields_dict = self.gathering_input_fields(inp_fields_elements={}, placeholders_dict=inp_dict_sub)
        print(f'\na Fail értékei:')
        for p in inpFields_dict.values():
            print(p)

        self.send_inputs(inpFields_dict, inp_dict_sub)

        ### Asserthez szükséges elvárt és tényleges értékek
        actual_str = self.popup_text(actual_str={})
        expected_str = self.expected_text(info='Fail')

        ## REG. ELLENŐRZÉSE NEGATÍV ÁGON - SIKERES SIKERTELEN REG. :))
        assert actual_str['reg_succ'] == expected_str['Title']
        assert actual_str['reg_succ_s'] == expected_str['Text']
        print(f"Assert a negatív ágon: {actual_str['reg_succ']} ({actual_str['reg_succ_s']})")

    @allure.id('TC1.2 P+')
    @allure.title('Regisztráció - fix adatokkal (samsara!)')
    def test_sign_up_fix_poz(self):
        ### belépési kisérlet jelszó nélkül - direkt negatív ág

        self.useRegistrationButton()

        ### Inputmezők kigyűjtése és elküldése
        inp_dict_sub = self.inp_values(sub_dict='Pass')
        inpFields_dict=self.gathering_input_fields(inp_fields_elements={})
        self.send_inputs(inpFields_dict, inp_dict_sub)

        ### Asserthez szükséges elvárt és tényleges értékek
        actual_str=self.popup_text(actual_str={})
        expected_str=self.expected_text(info='While')

        ## REG. ELLENŐRZÉSE POZITÍV ÁGON - SIKERES REG.
        assert actual_str['reg_succ'] == expected_str['Title']
        assert actual_str['reg_succ_s'] == expected_str['Text']
        print(f"Assert a pozitív ágon: {actual_str['reg_succ']} ({actual_str['reg_succ_s']})")

    @allure.id('TC1.3 cond P+ ')
    @allure.title('Regisztráció - Míg sikeres nem lesz')
    def test_sign_up_while(self):

        self.useRegistrationButton()

        inp_dict_sub = self.inp_values(sub_dict='While')
        inpFields_dict = self.gathering_input_fields(inp_fields_elements={})

        ### Asserthez szükséges elvárt és tényleges értékek
        expected_Pstr = self.expected_text(info='Pass')
        popup_title=''

        n = 1
        while popup_title != expected_Pstr['Title']:

            self.send_inputs(inpFields_dict, inp_dict_sub)

            actual_str = self.popup_text(actual_str={})
            expected_Fstr = self.expected_text(info='Pass')
            popup_title=actual_str['reg_succ']

            if actual_str['reg_succ'] == expected_Fstr['Title']:
                ### REG. ELLENŐRZÉSE INDIREKT NEGATÍV ÁGON - SIKERTELEN REG.
                assert actual_str['reg_succ'] == expected_Fstr['Title']
                assert actual_str['reg_succ_s'] == expected_Fstr['Text']
                ### Alábbi csak a konzolos 'többletinfó' kiíratáshoz szükséges
                reg_succ_N = expected_Fstr['Title']
                reg_succ_s_N = expected_Fstr['Text']

                ### Új belépési adatokat generálása n érték növelésével mivel az adott 'user#n' név már foglalt volt
                n += 1
                inp_dict_sub.update({'Username': f'user{n}',
                              'Email': f'user{n}@hotmail.com',})

                self.popup_ok_btn()

            else:
                if n == 1:
                    ### Alábbi csak a konzolos 'többletinfó' kiíratáshoz szükséges
                    actual_str['reg_succ'] = 'Sikeres regisztráció'
                    reg_succ_s_N = 'elsőre'

                ### REG. ELLENŐRZÉSE POZITÍV ÁGON - SIKERES REG.
                assert actual_str['reg_succ'] == expected_Pstr['Title']
                assert actual_str['reg_succ_s'] == expected_Pstr['Text']
                if actual_str['reg_succ'] == expected_Pstr['Title']:
                    print(f'\n{n - 1} negatív ágon lefuttatott Assert: {reg_succ_N} ({reg_succ_s_N}) után: ')
                    print(f"Assert a pozitív ágon: {actual_str['reg_succ']} ({actual_str['reg_succ_s']})")



    @allure.id('TC2. P+')
    @allure.title('Belépés sikerességének ellenőrzése')
    def test_sign_in(self):
        self.useSignInButton()


