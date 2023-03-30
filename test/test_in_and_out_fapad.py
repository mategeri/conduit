### 2. sign in automatizálása
### 11. sign out automatizálása

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

### F2:

def msg_frame(msg, frame='~'):
    print(frame * (len(msg) + 4))  # stringnél a szorzás ismétlést jelent
    print(f'# {msg} #')
    print(frame * (len(msg) + 4))

def mnu_elemek_ell(goal, mnu_nr):
    # print(f'\nFejlécmenű info: ha-> 3 elemű: Látogató (nincs belépve); ha-> 5 elemű: Felhasználó (belépett), ez most: {menusor_hossz}')
    login_status = {
        3: {'user': 'Látogató', 'status': 'nincs belépve'},
        5: {'user': 'Felhasználó', 'status': 'belépett'},
    }
    print(f'\n{goal}:'
          f'\nMenűelemek száma: {mnu_nr}  '
          f'\n-->> user: {login_status[mnu_nr]["user"]}, '
          f'\n     jogosultság: {login_status[mnu_nr]["status"]}\n')


def sign_in(Email, Password):
    # 1.: fejlécmenű login pontja -> keres, klikkel
    WebDriverWait(browser, 5).until(EC.presence_of_element_located((By.XPATH, '//a[@href="#/login"]')))
    sign_in_mnu_btn = browser.find_element(By.XPATH, '//a[@href="#/login"]')
    sign_in_mnu_btn.click()

    # 2.: felugró ablak -> elemek kitöltése
    input_Email = browser.find_element(By.XPATH, '//input[@placeholder="Email"]')
    input_password = browser.find_element(By.XPATH, '//input[@placeholder="Password"]')
    input_Email.send_keys(Email)
    input_password.send_keys(Password)
    WebDriverWait(browser, 5).until(EC.element_to_be_clickable((By.XPATH, '//button[@class="btn btn-lg btn-primary pull-xs-right"]')))
    sign_in_btn = browser.find_element(By.XPATH, '//button[@class="btn btn-lg btn-primary pull-xs-right"]')
    sign_in_btn.click()

    # 3.: login/logout státusz a fejlécmenű elemeinek száma alapján
    time.sleep(1) # késleltetés nélkül - csupán WebDriverWait-el - nem megfelelő a működés
    # WebDriverWait(browser, 5).until(EC.visibility_of_all_elements_located((By.XPATH,'//ul[@class="nav navbar-nav pull-xs-right"]//li[@class="nav-item"]')))
    # user_prof_btns_aft_click = browser.find_elements(By.XPATH,'//ul[@class="nav navbar-nav pull-xs-right"]//li[@class="nav-item"]')
    user_prof_btns_aft_click = WebDriverWait(browser, 5).until(EC.presence_of_all_elements_located((By.XPATH,'//ul[@class="nav navbar-nav pull-xs-right"]//li[@class="nav-item"]')))
    menusor_hossz = len(user_prof_btns_aft_click)



    if (menusor_hossz == 3): # sikertelen belépés
        WebDriverWait(browser, 5).until(EC.presence_of_element_located((By.XPATH, '//div[@class="swal-text"]')))
        # signin_res_text = browser.find_element(By.XPATH, '//div[@class="swal-text"]').text
        # print(f'if: "{signin_res_text}":')
        signin_fail = browser.find_element(By.XPATH, '//div[@class="swal-title"]').text
        assert signin_fail == 'Login failed!'
        msg_frame(f'LogIN "-" ág assert 1.: Sikertelen belépés figyelmeztető üzenet: "{signin_fail}"', '-')
        OK_button = browser.find_element(By.XPATH, '//button[@class="swal-button swal-button--confirm"]')
        OK_button.click()
        mnu_elemek_ell('Belépés sikerességének ellenőrzése "-" ág', menusor_hossz)

    elif (menusor_hossz == 5): # sikeres belépés
        mnu_elemek_ell('Belépés sikerességének ellenőrzése "+" ág', menusor_hossz)
        assert menusor_hossz == 5  # assert menusor_hossz == 5  # Pozitív ág belépésre: belépést követően a fejlécmenű elemei 5-re változnak
        if (menusor_hossz == 5):
            msg_frame(f'LogIN "+" ág ellenőrzése: menuelemek száma {menusor_hossz} -> Belépés megvalósult!')

        ### assert "Log out" gomb meglétének ellenőrzésével
        find_log_out_btn = WebDriverWait(browser, 5).until(EC.presence_of_element_located((By.XPATH, '//i[@class="ion-android-exit"]')))
        assert find_log_out_btn
        msg_frame(f'LogIN "+" ág assert 1.-> igazolt belépés: A kilépés gomb lokalizálható!', '+')

        ### assert "Log out" felírat meglétének ellenőrzésével
        user_prof_btns = browser.find_elements(By.XPATH, '//ul[@class="nav navbar-nav pull-xs-right"]//li[@class="nav-item"]')
        log_out_btn_txt = user_prof_btns[-1].text
        # print(log_out_btn_txt)
        conf_text = (log_out_btn_txt.replace(' ', '')).upper()
        # print(conf_text)
        assert conf_text == 'LOGOUT'
        msg_frame(f'LogIN "+" ág assert 2. -> igazolt belépés: {log_out_btn_txt} szöveg megjelent!', '+')

        time.sleep(1)

        browser.refresh()
        mnu_elemek_ell('Refresh kilépés ellenőrzése "-" ág:',menusor_hossz)
        assert menusor_hossz == 5 # Negatív ág kilépésre: böngésző frissítés után is megmarad a belépett státusz
        if (menusor_hossz == 5):
            msg_frame(f'LogOUT "-" ág ellenőrzés -> böngésző frissítés nem okoz kilépést!', '-')

        find_log_out_btn = WebDriverWait(browser, 5).until(EC.presence_of_element_located((By.XPATH, '//i[@class="ion-android-exit"]')))
        find_log_out_btn.click()

        user_prof_btns_aft_click = WebDriverWait(browser, 5).until(EC.presence_of_all_elements_located(
            (By.XPATH, '//ul[@class="nav navbar-nav pull-xs-right"]//li[@class="nav-item"]')))
        menusor_hossz = len(user_prof_btns_aft_click)
        mnu_elemek_ell('Kilépés ellenőrzése', menusor_hossz)
        assert menusor_hossz == 3 # assert menusor_hossz == 3  # Pozitív ág kilépésre: kilépést követően a fejlécmenű elemei 3-ra csökkennek
        if (menusor_hossz == 3):
            msg_frame(f'LogOUT "+" ág ellenőrzés: menuelemek száma {menusor_hossz} -> Kilépés megvalósult!')


### függvény meghívás értékekkel
### Pozitív ág: Belépés valós adatokkal ### Negatív ág: Kilépés valós adatokkal ### Pozitív ág: Belépés valós adatokkal
sign_in('user2@hotmail.com', 'Userpass1')

### Negatív ág: Belépési kisérlet nem megfelelő user adatokkal -> hibás jelszóval
sign_in('user2@hotmail.com', 'Userpass2')

# böngésző bezárása
browser.quit()