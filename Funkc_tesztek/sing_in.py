## 1. sign in automatizálása

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


def sign_in(Email, Password):
    WebDriverWait(browser, 5).until(EC.presence_of_element_located((By.XPATH, '//a[@href="#/login"]')))
    sign_in_mnu_btn = browser.find_element(By.XPATH, '//a[@href="#/login"]')
    sign_in_mnu_btn.click()

    # input_Username = browser.find_element(By.XPATH, '//input[@placeholder="Username"]')

    input_Email = browser.find_element(By.XPATH, '//input[@placeholder="Email"]')
    input_password = browser.find_element(By.XPATH, '//input[@placeholder="Password"]')

    # input_Email.clear()
    input_Email.send_keys(Email)
    # input_password.clear()
    input_password.send_keys(Password)

    sign_in_btn = browser.find_element(By.XPATH, '//button[@class="btn btn-lg btn-primary pull-xs-right"]')
    WebDriverWait(browser, 5).until(EC.element_to_be_clickable((By.XPATH, '//button[@class="btn btn-lg btn-primary pull-xs-right"]')))
    time.sleep(1)
    sign_in_btn.click()

    # WebDriverWait(browser, 5).until(EC.presence_of_element_located((By.XPATH, '//div[@class="swal-text"]')))
    WebDriverWait(browser, 5).until(EC.presence_of_element_located((By.XPATH, '//div[@class="swal-text"]')))
    time.sleep(1)
    signin_res_text = browser.find_element(By.XPATH, '//div[@class="swal-text"]').text
    # signin_res_text = signin_res.text
    # Userbelépés adataira kapott válasz kiíratása
    # print(signin_res)
    # print(type(signin_res))
    print(signin_res_text)
    print(type(signin_res_text))

    # assert a kilépés gomb jelenlétének igazolásával
    # find_log_out_btn = WebDriverWait(browser, 5).until(EC.presence_of_element_located((By.XPATH, '//i[@class="ion-android-exit"]')))

    if (signin_res_text == 'Invalid user credentials.'):
        print(f'if: {signin_res_text}')
        signin_fail = browser.find_element(By.XPATH, '//div[@class="swal-title"]').text
        print(f'Sikertelen belépés - sikeres tesz negatív ágon - eredménye: "{signin_fail}"')
        assert signin_fail == 'Login failed!'

    else:
        print(f'else: {signin_res_text}')
        # WebDriverWait(browser, 5).until(EC.presence_of_element_located((By.XPATH, '//i[@class="ion-android-exit"]')))
        find_log_out_btn = WebDriverWait(browser, 5).until(EC.presence_of_element_located((By.XPATH, '//i[@class="ion-android-exit"]')))
        assert find_log_out_btn
        msg_frame(f'A kilépés gomb megvan!')
        # print(find_log_out_btn)
        # assert "Log out" felírat meglétének ellenőrzésével
        user_prof_btns = browser.find_elements(By.XPATH, '//ul[@class="nav navbar-nav pull-xs-right"]//li[@class="nav-item"]')
        # print(user_prof_btns)
        log_out_btn_txt = user_prof_btns[-1].text
        # print(log_out_btn_txt)
        conf_text = (log_out_btn_txt.replace(' ', '')).upper()
        print(conf_text)
        msg_frame(f'{log_out_btn_txt} <=> {conf_text}: igazolt a belépett állapotot jelző "Log out" szöveg jelenléte!')
        assert conf_text == 'LOGOUT'

        time.sleep(2)
        find_log_out_btn.click()
        #browser.refresh()


### függvény meghívás értékekkel
### Pozitív ág: Belépés valós adatokkal
sign_in('user1@hotmail.com', 'Userpass1')

### Negatív ág: Belépési kisérlet nem megfelelő user adatokkal -> hibás jelszóval
sign_in('user2@hotmail.com', 'Userpass1')

# böngésző bezárása
# browser.quit()
