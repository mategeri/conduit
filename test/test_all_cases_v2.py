import time
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
        # placeholders = ["Username", "Email", "Password"] # a kód kezdeti fázisban előre def. értékekkel ment
        # print(placeholders)
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
        # inputmezők kitöltése és küldése fgv-ből nyert dict-ek kulcs/érték átadásával
        for pairs in inpFields_dict.items():
            inpName = pairs[0]
            inpValue = pairs[1]
            # print(f'key&value: {inpName}={inpValue}') # ellenőrző sor
            send_this_key = inp_dict_sub[inpName]
            inpValue.send_keys(send_this_key)

        WebDriverWait(self.browser, 5).until(
            EC.presence_of_element_located(
                (By.XPATH, '//button[@class="btn btn-lg btn-primary pull-xs-right"]'))).click()

    def reg_process_init(self, keyword:str):
        ### reg. folyamat indítása menűpont kattintásával
        self.useRegistrationButton()

        ### Input értékek kigyűjtése, mezők kitöltése és elküldése
        inp_dict_sub = self.inp_values(sub_dict=keyword)
        inpFields_dict = self.gathering_input_fields(inp_fields_elements={}, placeholders_dict=inp_dict_sub)
        self.send_inputs(inpFields_dict, inp_dict_sub)



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
                        "Accept": {'Text': 'I accept!'},
                        }
        return expected_str[info]

    def popup_ok_btn(self):
        WebDriverWait(self.browser, 5).until(
            EC.presence_of_element_located((By.XPATH, '//button[@class="swal-button swal-button--confirm"]'))).click()


    # def check_mnuitems_length(self):
    #     nav_mnu_items = WebDriverWait(self.browser, 5).until(EC.presence_of_all_elements_located(
    #         (By.XPATH, '//ul[@class="nav navbar-nav pull-xs-right"]//li[@class="nav-item"]')))
    #     menusor_hossz = len(nav_mnu_items)
    #     # print(menusor_hossz)
    #     return menusor_hossz

    def locate_navbar_items(self):
        navbar_items = WebDriverWait(self.browser, 5).until(EC.presence_of_all_elements_located(
            (By.XPATH, '//ul[@class="nav navbar-nav pull-xs-right"]//li[@class="nav-item"]')))
        return navbar_items


    def signin_rutin(self):
        self.useSignInButton()
        inp_dict_sub = self.inp_values(sub_dict='Pass')
        del inp_dict_sub['Username']
        # print(inp_dict_sub)
        inpFields_dict = self.gathering_input_fields(inp_fields_elements={}, placeholders_dict=inp_dict_sub)
        self.send_inputs(inpFields_dict, inp_dict_sub)

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

    def teardown_method(self):
        pass
        # self.browser.quit()

# TC1: Regisztráció----------------------------------------------------------------------------------------------------------------------
    @allure.id('TC1.1. N+')
    @allure.title('Regisztrációs kisérlet - jelszó nélkül')
    def test_sign_up_direct_neg(self):
        ### belépési kisérlet jelszó nélkül - direkt negatív ág

        self.reg_process_init(keyword='Fail')

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
        ### belépési kisérlet előre megadott (még nem foglalt) adatokkal

        self.reg_process_init(keyword='Pass')

        ### Asserthez szükséges elvárt és tényleges értékek
        actual_str=self.popup_text(actual_str={})
        expected_str=self.expected_text(info='Pass')

        ## REG. ELLENŐRZÉSE POZITÍV ÁGON - SIKERES REG.
        assert actual_str['reg_succ'] == expected_str['Title']
        assert actual_str['reg_succ_s'] == expected_str['Text']
        print(f"Assert a pozitív ágon: {actual_str['reg_succ']} ({actual_str['reg_succ_s']})")

    @allure.id('TC1.3 cond P+ ')
    @allure.title('Regisztráció - Míg sikeres nem lesz')
    def test_sign_up_while(self):
        ### regisztrációs folyamat ciklussal, arra az esetre, ha a megelöző felhasználó név már foglalt lenne

        ### reg. folyamat indítása menűpont kattintásával
        self.useRegistrationButton()

        ### Inputmezők adatainak kigyűjtése - küldés a while cikluson belül
        inp_dict_sub = self.inp_values(sub_dict='While')
        inpFields_dict = self.gathering_input_fields(inp_fields_elements={}, placeholders_dict=inp_dict_sub)

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
                    ### Alábbi csak a konzolos 'többletinfó' kiíratáshoz szükséges
                    print(f'\n{n - 1} negatív ágon lefuttatott Assert: {reg_succ_N} ({reg_succ_s_N}) után: ')
                    print(f"Assert a pozitív ágon: {actual_str['reg_succ']} ({actual_str['reg_succ_s']})")

# TC2: Bejelentkezés --------------------------------------------------------------------------------------------------------------------
    @allure.id('TC2. P+')
    @allure.title('Belépés sikerességének ellenőrzése')
    def test_sign_in(self):
        ### Sikeres bejelentkezés ellenőrzése
        # belépési rutin folyamat
        self.signin_rutin()

        time.sleep(2)
        self.browser.refresh()
        navbar_items=self.locate_navbar_items()
        menusor_hossz = len(navbar_items)
        if menusor_hossz == 5:  # sikeres belépés
            # Pozitív ág belépésre: belépést követően a fejlécmenű elemei 5-re változnak
            assert menusor_hossz == 5
            print(f'\nLogIN "+" ág ellenőrzése: menuelemek száma {menusor_hossz} -> Belépés megvalósult!')

            ### assert "Log out" gomb meglétének ellenőrzésével
            find_log_out_btn = WebDriverWait(self.browser, 5).until(
                EC.presence_of_element_located((By.XPATH, '//i[@class="ion-android-exit"]')))
            assert find_log_out_btn
            print(f'LogIN "+" ág assert 1.-> igazolt belépés: A kilépés gomb lokalizálható!', '+')

            ### assert "Log out" felírat meglétének ellenőrzésével
            log_out_btn_txt = navbar_items[-1].text
            # conf_text = (log_out_btn_txt.replace(' ', '')).upper()
            # assert conf_text == 'LOGOUT'
            assert log_out_btn_txt == ' Log out'
            print(f'LogIN "+" ág assert 2. -> igazolt belépés: "{log_out_btn_txt}" szöveg megjelent!', '+')

# TC3: Adatkezelési nyilatkozat használata ----------------------------------------------------------------------------------------------
    @allure.id('TC3. P+')
    @allure.title('Cookie policy acceptance')
    def test_gdpr_acceptance(self):
        ### 3.	Adatkezelési nyilatkozat használata

        #belépési rutin folyamat
        self.signin_rutin()

        ### sütihasználati politikát elfogadó gomb
        accept_btn= WebDriverWait(self.browser, 5).until(EC.presence_of_element_located((By.XPATH, '//button[@class="cookie__bar__buttons__button cookie__bar__buttons__button--accept"]/div')))

        ### Öszzevetésre szánt gombfelíratok
        accept_btn_text=accept_btn.text
        expected_str = self.expected_text(info='Accept')
        ## cookie policy elfogadásához tartotzó gomb szövegének ellenőrzése - 'I accept!' gomb
        assert accept_btn_text == expected_str['Text']

        accept_btn.click()

# TC4:	Adatok listázása-----------------------------------------------------------------------------------------------------------------



# TC5: Több oldalas lista bejárása-------------------------------------------------------------------------------------------------------


# TC6: Új adat bevitel-------------------------------------------------------------------------------------------------------------------


# TC7: Ismételt és sorozatos adatbevitel adatforrásból-----------------------------------------------------------------------------------


# TC8: Meglévő adat módosítás------------------------------------------------------------------------------------------------------------


# TC9: Adat vagy adatok törlése----------------------------------------------------------------------------------------------------------


# TC10:	Adatok lementése felületről------------------------------------------------------------------------------------------------------


# TC11:	Kijelentkezés--------------------------------------------------------------------------------------------------------------------
    @allure.id('TC11. P+')
    @allure.title('Kilépés sikerességének ellenőrzése')
    def test_sign_out(self):
        ### Sikeres Kijelentkezés ellenőrzése
        # belépési rutin folyamat
        self.signin_rutin()

        time.sleep(2)
        self.browser.refresh()
        navbar_items = self.locate_navbar_items()
        menusor_hossz = len(navbar_items)

        if menusor_hossz == 5:  # sikeres belépés
            assert menusor_hossz == 5
            print(f'\nMenuelemek száma: {menusor_hossz} -> Belépés megvalósult!')
            WebDriverWait(self.browser, 5).until(
                EC.presence_of_element_located((By.XPATH, '//i[@class="ion-android-exit"]'))).click()

        # self.browser.refresh()
        navbar_items = self.locate_navbar_items()
        menusor_hossz = len(navbar_items)
        if menusor_hossz == 3:  # sikeres belépés
            assert menusor_hossz == 3
            print(f'LogOUT "+" ág ellenőrzése: menuelemek száma {menusor_hossz} -> Kilépés megvalósult!')
            find_login_btn=WebDriverWait(self.browser, 5).until(
                EC.presence_of_element_located((By.XPATH, '//a[@href="#/login"]')))
            assert find_login_btn
            ### assert "Log out" felírat meglétének ellenőrzésével
            # user_prof_btns = self.browser.find_elements(By.XPATH,
            #                                             '//ul[@class="nav navbar-nav pull-xs-right"]//li[@class="nav-item"]')
            sign_in_btn_txt = navbar_items[-2].text
            # conf_text = (log_out_btn_txt.replace(' ', '')).upper()
            # assert conf_text == 'LOGOUT'
            assert sign_in_btn_txt == 'Sign in'
            print(f'LogIN "+" ág assert 2. -> igazolt belépés: "{sign_in_btn_txt}" szöveg megjelent!', '+')
















