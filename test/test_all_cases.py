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

    # def fuggveny(self):
    #     a = 10
    #     b = 'Valami'
    #
    #     # result = [a, b]
    #     # result = []
    #     # result.append(a)
    #     # result.append(b)
    #     # return result # Lista jön vissza [10, 'Valami']
    #
    #     return a, b # Tuple --> valtozo = fuggveny() --> valtozo = (10, 'Valami') || a, b = fuggveny()
    def getRegistrationButton(self):
        return WebDriverWait(self.browser, 5).until(
            EC.presence_of_element_located((By.XPATH, '//a[@href="#/register"]')))

        # sign_up_mnu_btn = self.browser.find_element(By.XPATH, '//a[@href="#/register"]')
        # sign_up_mnu_btn.click()

    def gathering_input_fields(self, inp_fields_elements):
        # user = self.browser.find_element(By.XPATH, '//input[@placeholder="Username"]')
        # mail = self.browser.find_element(By.XPATH, '//input[@placeholder="Email"]')
        # passw = self.browser.find_element(By.XPATH, '//input[@placeholder="Password"]')
        placeholders =["Username","Email","Password"]
        inp_fields_name=[]
        # inp_fields_elements={}
        for field in range(len(placeholders)):
            # inp_fields_name[f]=f'inp_{placeholders[f]}'
            # print(inp_fields_name)
            inp_fields_elements[f'{placeholders[field]}']=self.browser.find_element(By.XPATH, f'//input[@placeholder="{placeholders[field]}"]')
            # print(inp_fields_elements)

        # input_Username = self.browser.find_element(By.XPATH, '//input[@placeholder="Username"]')
        # input_Email = self.browser.find_element(By.XPATH, '//input[@placeholder="Email"]')
        # input_password = self.browser.find_element(By.XPATH, '//input[@placeholder="Password"]')
        #
        # inp_fields = list()
        # inp_fields.append(input_Username)
        # inp_fields.append(input_Email)
        # inp_fields.append(input_password)
        # print(f'\ngath_fgv elemei: {inp_fields}')

        # inp_fields_dict['Inputfield_username']=input_Username
        # inp_fields_dict['Inputfield_email']=input_Email
        # inp_fields_dict['Inputfield_password']=input_password
        # print(f'\ngath_fgv Dict elemei: {inp_fields_dict}')
        return inp_fields_elements

    def inp_values(self, inp_dict):
        inp_dict = {"Pass": {'Username': 'user1',
                             'Email': 'user1@hotmail.com',
                             'Password': 'Userpass1', },
                    "Fail": {'Username': 'user1',
                             'Email': 'user1@hotmail.com',
                             'Password': '', }}
        # inp_list = ['user1', 'user1@hotmail.com', 'Userpass1']
        # print(f'\nInp value fgv >> dict: {inp_dict} \n list: {inp_list}>')
        return inp_dict

    # self.gathering_input_fileds()
    # print(self.gathering_input_fileds())
    # for inp_fld, inp_value in inp_fields.items():
    #     inp_fld = inp_value

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

        self.registration_button = self.getRegistrationButton()

        # WebDriverWait(self.browser, 5).until(EC.presence_of_element_located((By.XPATH, '//a[@href="#/register"]')))
        # sign_up_mnu_btn = self.browser.find_element(By.XPATH, '//a[@href="#/register"]')
        # sign_up_mnu_btn.click()

    def teardown_method(self):
        pass
        # self.browser.quit()

    @allure.id('TC1 +Ág')
    @allure.title('Regisztráció - Míg sikeres nem lesz')
    def test_sign_up_npoz(self, Username_n=['user1'], Email_n=['user1@hotmail.com'], Password='Userpass1', reg_succ=''):

        # WebDriverWait(self.browser, 5).until(EC.presence_of_element_located((By.XPATH, '//a[@href="#/register"]')))
        # sign_up_mnu_btn = self.browser.find_element(By.XPATH, '//a[@href="#/register"]')
        # sign_up_mnu_btn.click()
        self.registration_button.click()

        ### Inputmezők kigyűjtése
        # input_Username = self.browser.find_element(By.XPATH, '//input[@placeholder="Username"]')
        # input_Email = self.browser.find_element(By.XPATH, '//input[@placeholder="Email"]')
        # input_password = self.browser.find_element(By.XPATH, '//input[@placeholder="Password"]')

        inpFields_dict= self.gathering_input_fields(inp_fields_elements={})
        print(inpFields_dict)
        # self.inpFields = self.gathering_input_fields(inp_fields=())
        # print(f'Inputfields dict: {self.inpFields}')
        # inp_elemek = self.gathering_input_fileds(inp_fields=[])
        # input_value_elemek = self.inp_values(inp_dict={}, inp_list=[])
        # input_value_elemek = self.inp_values(inp_dict={})
        # inp_dict_in = input_value_elemek[0]
        # inp_dict_inP = inp_dict_in['Pass']
        # print(inp_dict_in)
        # for child in inp_dict_in.values():
        #     print(child)
        #     for x in child.items():
        #         print(x[0])
        #         print(x[1])

        for pairs in inpFields_dict.items():
            print(pairs[0])
            print(pairs[1])

        input_value_elemek = self.inp_values(inp_dict={})
        inp_dict_inP = input_value_elemek['Pass']
        print(f'\ncsak a Pass értékei:')
        for p in inp_dict_inP.values():
            print(p)

        # inp_list_in = input_value_elemek[1]
        # print(inp_list_in)
        # for y in inp_list_in:
        #     print(y)
        # input_fields_elemek = self.gathering_input_fileds(inp_fields_dict={})
        # print(f'\nItt a gather{input_fields_elemek}\naz első:{input_fields_elemek[0]}')
        # print(f'\na második:{input_fields_elemek[1]}')

        # n = 1
        # inp_values = ['user1', 'user1@hotmail.com', 'Userpass1']
        # ### Regisztrációs kisérlet-lánc default adatokkal, míg sikeres nem lesz
        # while reg_succ != 'Welcome!':
        #     ### inputmezők kitöltése
        #     input_fileds_elemek[0].send_keys(Username_n[-1])
        #     input_fileds_elemek[1].send_keys(Email_n[-1])
        #     input_fileds_elemek[2].send_keys(Password)
        #
        #     sign_up_btn = WebDriverWait(self.browser, 5).until(
        #         EC.presence_of_element_located((By.XPATH, '//button[@class="btn btn-lg btn-primary pull-xs-right"]')))
        #     assert sign_up_btn.is_displayed()
        #     sign_up_btn.click()
        #
        #     WebDriverWait(self.browser, 5).until(
        #         EC.presence_of_element_located((By.XPATH, '//div[@class="swal-title"]')))
        #     reg_succ = self.browser.find_element(By.XPATH, '//div[@class="swal-title"]').text
        #     reg_succ_s = self.browser.find_element(By.XPATH, '//div[@class="swal-text"]').text
        #
        #     if reg_succ == 'Registration failed!':
        #         ### REG. ELLENŐRZÉSE INDIREKT NEGATÍV ÁGON - SIKERTELEN REG.
        #         assert reg_succ == 'Registration failed!'
        #         assert reg_succ_s == 'Email already taken.'
        #         reg_succ_N = reg_succ
        #         reg_succ_s_N = reg_succ_s
        #
        #         ### Új belépési adatokat generálása n érték növelésével mivel az adott 'usern' név már foglalt volt
        #         n += 1
        #         Username_n.append(f'user{str(n)}')
        #         Email_n.append(f'user{str(n)}@hotmail.com')
        #         # inp_values[0] = f'user{str(n)}'
        #         # inp_values[1] = f'user{str(n)}@hotmail.com'
        #         # print(f'\n új inputok: {inp_values[0]}, email: {inp_values[1]}')
        #
        #
        #         ok_btn = WebDriverWait(self.browser, 5).until(
        #             EC.presence_of_element_located((By.XPATH, '//button[@class="swal-button swal-button--confirm"]')))
        #         ok_btn.click()
        #
        #     else:
        #         if n == 1:
        #             reg_succ_N = 'Sikeres regisztráció'
        #             reg_succ_s_N = 'elsőre'
        #
        #
        #         ### REG. ELLENŐRZÉSE POZITÍV ÁGON - SIKERES REG.
        #         assert reg_succ == 'Welcome!'
        #         assert reg_succ_s == 'Your registration was successful!'
        #         if reg_succ == 'Welcome!':
        #             print(f'\n{n - 1} negatív ágon lefuttatott Assert: {reg_succ_N} ({reg_succ_s_N}) után: ')
        #             print(f"Assert a pozitív ágon: {reg_succ} ({reg_succ_s})")

        # böngésző bezárása
        self.browser.quit()

    @allure.id('TC2 ')
    @allure.title('Regisztrációs kisérlet - jelszó nélkül')
    def test_sign_up_direct_neg(self):
        ### belépési kisérlet jelszó nélkül - direkt negatív ág

        # WebDriverWait(self.browser, 5).until(EC.presence_of_element_located((By.XPATH, '//a[@href="#/register"]')))
        # sign_up_mnu_btn = self.browser.find_element(By.XPATH, '//a[@href="#/register"]')
        # sign_up_mnu_btn.click()
        self.registration_button.click()

        ### Inputmezők kigyűjtése
        # input_fields_elemek = self.gathering_input_fileds(inp_fields_dict={})
        # print(f'\nItt a gather{input_fields_elemek}\naz első:{input_fields_elemek[0]}')
        # print(f'\na második:{input_fields_elemek[1]}')

        input_value_elemek = self.inp_values(inp_dict={})
        inp_dict_inF = input_value_elemek['Fail']

        inpFields_dict = self.gathering_input_fields(inp_fields_elements={})
        print(inpFields_dict)
        for pairs in inpFields_dict.items():
            inpName = pairs[0]
            inpValue=pairs[1]
            print(f'key&value: {inpName}={inpValue}')
            send_this_key=inp_dict_inF[inpName]
            print(send_this_key)
            # print(f'def details: {inp_dict_inF[inpName]}')
            inpValue.send_keys(send_this_key)




        # Username = self.browser.find_element(By.XPATH, '//input[@placeholder="Username"]')
        # Email = self.browser.find_element(By.XPATH, '//input[@placeholder="Email"]')
        # Password = self.browser.find_element(By.XPATH, '//input[@placeholder="Password"]')

        ### inputmezők kitöltése

        # ## Under Construction
        # input_value_elemek = self.inp_values(inp_dict={}, inp_list=[])
        # inp_dict_in = input_value_elemek[0]
        # inp_dict_inP = inp_dict_in['Fail']
        input_value_elemek = self.inp_values(inp_dict={})
        inp_dict_inP = input_value_elemek['Fail']
        print(f'\ncsak a Fail értékei:')
        for f in inp_dict_inP.values():
            print(f)
        # print(input_value_elemek['Fail'][''])

        # ## Under Construction
        # input_value_elemek = self.inp_values(inp_dict={}, inp_list=[])
        # inp_dict_in = input_value_elemek[0]
        # inp_dict_inP = inp_dict_in['Fail']
        # print(f'\nA Fail értékei:')
        # for p in inp_dict_inP.values():
        #     print(p)
        # print(f'username:{inp_dict_inP["input_Username"]}')
        # print(f'email:{inp_dict_inP["input_Email"]}')
        #
        # Username.send_keys(inp_dict_inP['input_Username'])
        # Email.send_keys(inp_dict_inP["input_Email"])
        # Password.send_keys('')

        # Username.send_keys('user1')
        # Email.send_keys('user1@hotmail.com')
        # Password.send_keys('')

        sign_up_btn = WebDriverWait(self.browser, 5).until(
            EC.presence_of_element_located((By.XPATH, '//button[@class="btn btn-lg btn-primary pull-xs-right"]')))
        assert sign_up_btn.is_displayed()
        sign_up_btn.click()

        WebDriverWait(self.browser, 5).until(EC.presence_of_element_located((By.XPATH, '//div[@class="swal-title"]')))
        reg_succ = self.browser.find_element(By.XPATH, '//div[@class="swal-title"]').text
        reg_succ_s = self.browser.find_element(By.XPATH, '//div[@class="swal-text"]').text

        if reg_succ == 'Registration failed!':
            ### REG. ELLENŐRZÉSE DIREKT NEGATÍV ÁGON - SIKERTELEN REG.
            assert reg_succ == 'Registration failed!'
            assert reg_succ_s == 'Password field required.'
            print(f'\nAssert direkt negatív ágon: {reg_succ} ({reg_succ_s})')
            ok_btn = WebDriverWait(self.browser, 5).until(
                EC.presence_of_element_located((By.XPATH, '//button[@class="swal-button swal-button--confirm"]')))
            ok_btn.click()

        # böngésző bezárása
        # self.browser.quit()
