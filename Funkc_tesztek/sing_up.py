## 1. Sing up automatizálása

from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
import time

service = Service(executable_path=ChromeDriverManager().install())
options = Options()
options.add_experimental_option("detach", True)
browser = webdriver.Chrome(service=service, options=options)

# oldal elérés
URL = 'http://localhost:1667/'
browser.get(URL)

### F1:


def msg_frame(msg, frame='-'):
    print(frame * (len(msg) + 4))  # stringnél a szorzás ismétlést jelent
    print(f'| {msg} |')
    print(frame * (len(msg) + 4))

Username_n = ['user1']
# Password = 'Userpass1'
Email_n = ['user1@hotmail.com']

def user_data(n):
    Username = 'user'+str(n)
    Username_n.append(Username)
    Email = 'user'+str(n)+'@hotmail.com'
    Email_n.append(Email)
    # print(f'külső fgv: Username:{Username}, email: {Email}') # adatellenőrzés adatok kííratásával


def Sing_up(Username, Email, Password):
    WebDriverWait(browser, 5).until(EC.presence_of_element_located((By.XPATH, '//a[@href="#/register"]')))
    sing_up_mnu_btn = browser.find_element(By.XPATH, '//a[@href="#/register"]')
    sing_up_mnu_btn.click()

    input_Username = browser.find_element(By.XPATH, '//input[@placeholder="Username"]')
    input_Email = browser.find_element(By.XPATH, '//input[@placeholder="Email"]')
    input_password = browser.find_element(By.XPATH, '//input[@placeholder="Password"]')

    reg_succ = ''
    n = 1

    while reg_succ != 'Welcome!':
        input_Username.send_keys(Username_n[-1])
        input_Email.send_keys(Email_n[-1])
        input_password.send_keys(Password)

        WebDriverWait(browser, 5).until(
        EC.presence_of_element_located((By.XPATH, '//button[@class="btn btn-lg btn-primary pull-xs-right"]')))
        sing_up_btn = browser.find_element(By.XPATH, '//button[@class="btn btn-lg btn-primary pull-xs-right"]')
        assert sing_up_btn.is_displayed()
        # if sing_up_btn.is_displayed():    # a belépéshez szükséges gomb meglétének ellenőrzése
        #     msg_frame('SING UP button assert -->  :)')
        sing_up_btn.click()

        WebDriverWait(browser, 5).until(EC.presence_of_element_located((By.XPATH, '//div[@class="swal-title"]')))
        reg_succ = browser.find_element(By.XPATH, '//div[@class="swal-title"]').text
        reg_succ_s = browser.find_element(By.XPATH, '//div[@class="swal-text"]').text
        # Userbelépés adataira kapott válasz kiíratása
        # print(reg_succ)
        # print(reg_succ_s)

        if reg_succ == 'Registration failed!':
            ### REG. ELLENŐRZÉSE NEGATÍV ÁGON - SIKERTELEN REG.
            assert reg_succ == 'Registration failed!'
            assert reg_succ_s == 'Email already taken.'
            msg_frame(f'"Assert negatív ágon: {n}. sikertelen regisztráció"')

            # msg_frame("Registration failed!") # SIKERTELEN REG. üzenet
            # msg_frame(f'Belépésnél használt értékek: Username:{Username}, email: {Email}')

            ### Új belépési adatokat generáló fgv meghívása
            # n értékének növelése, mivel az adott 'usern' név már foglalt volt
            n += 1
            user_data(n)
            WebDriverWait(browser,5).until(EC.presence_of_element_located((By.XPATH, '//button[@class="swal-button swal-button--confirm"]')))
            ok_btn = browser.find_element(By.XPATH, '//button[@class="swal-button swal-button--confirm"]')
            ok_btn.click()

        elif reg_succ == 'Welcome!':
            ### REG. ELLENŐRZÉSE POZITÍV ÁGON - SIKERES REG.
            assert reg_succ == 'Welcome!'
            assert reg_succ_s == 'Your registration was successful!'
            msg_frame("Assert pozitív ágon: Sikeres regisztráció", '*')


### függvény meghívás értékekkel
Sing_up(Username_n[-1], Email_n[-1], 'Userpass1')

# böngésző bezárása
# browser.quit()
