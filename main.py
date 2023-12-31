import os
import sys
import zipfile

import undetected_chromedriver as uc
from selenium.common import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.wait import WebDriverWait


# Prevent closing browser after complete registration
class MyUDC(uc.Chrome):
    def __del__(self):
        try:
            self.service.process.kill()
        except:  # noqa
            pass
        # self.quit()


def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


def extract_zip(path):
    extension_name = path.split('.')[0]
    print(f"Extracting {path} in path {os.getcwd()}...")
    with zipfile.ZipFile(path, 'r') as zip_ref:
        # Create folder for extension
        if not os.path.exists(f"{extension_name}"):
            os.mkdir(f"{extension_name}")

        zip_ref.extractall(f"{extension_name}")


def close_extension_start_page(driver):
    driver.switch_to.window(driver.window_handles[0])
    driver.close()
    driver.switch_to.window(driver.window_handles[0])


def initialize_driver():
    deepl_zip_path = resource_path('deepl.zip')

    extract_zip(deepl_zip_path)

    options = uc.ChromeOptions()
    deepl_folder_path = resource_path('deepl')
    options.add_argument(f'--load-extension={deepl_folder_path}')

    driver = MyUDC(debug=True, options=options, use_subprocess=True)

    close_extension_start_page(driver)

    return driver


def get_temp_email(driver, wait):
    driver.get('https://tempmail.plus/')
    email_name = wait.until(ec.presence_of_element_located((By.CSS_SELECTOR, "#pre_button"))).get_attribute('value')
    email_domain = wait.until(ec.presence_of_element_located((By.CSS_SELECTOR, "#domain"))).text
    new_email = email_name + email_domain
    return new_email


def register_to_phind(driver, wait, email):
    driver.switch_to.new_window()
    driver.get('https://www.phind.com/api/auth/signin')
    wait.until(ec.presence_of_element_located((By.CSS_SELECTOR, "#input-email-for-email-provider"))).send_keys(email)
    wait.until(ec.presence_of_element_located((By.CSS_SELECTOR, "#submitButton"))).click()


def confirm_email(driver, wait):
    driver.switch_to.window(driver.window_handles[0])
    while True:
        try:
            wait.until(ec.presence_of_element_located(
                (By.CSS_SELECTOR, "#container-body > div > div.inbox > div.mail"))).click()
            break
        except TimeoutException:
            driver.refresh()
    confirm_url = wait.until(ec.presence_of_element_located((By.CSS_SELECTOR,
                                                             "#info > div.overflow-auto.mb-20 > table > tbody > tr:nth-child(2) > td > table > tbody > tr > td > a"))).get_property(
        "href")
    return confirm_url


def click_confirmation_link(driver, confirm_url):
    driver.get(confirm_url)


def set_up_for_programming(driver, wait):
    wait.until(ec.presence_of_element_located((By.CSS_SELECTOR, "#Use\\ Best\\ Model"))).click()
    wait.until(ec.presence_of_element_located((By.CSS_SELECTOR, "#Pair\\ Programmer"))).click()


def main():
    driver = initialize_driver()
    wait = WebDriverWait(driver, 10)

    email = get_temp_email(driver, wait)
    register_to_phind(driver, wait, email)
    confirm_url = confirm_email(driver, wait)
    click_confirmation_link(driver, confirm_url)
    set_up_for_programming(driver, wait)


if __name__ == '__main__':
    main()
