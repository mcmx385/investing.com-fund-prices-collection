from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By

from config import *
from helpers.datetimes import last_year
import os
from dotenv import dotenv_values

envs = dotenv_values(".env")

USERNAME = envs["USERNAME"]
PASSWORD = envs["PASSWORD"]

print(USERNAME, PASSWORD)


def init_driver():
    try:
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("--disable-notifications")
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        # chrome_options.add_argument('--headless')
        chrome_options.add_argument('--window-size=1024,768')
        prefs = {
            "download.default_directory": DOWNLOAD_PATH,
            "download.prompt_for_download": False,
            "download.directory_upgrade": True,
            "safebrowsing.enabled": True,
            "helperApps.neverAsk.saveToDisk": 'text/csv',
            'download.manager.showWhenStarting': False
        }
        chrome_options.add_experimental_option("prefs", prefs)

        caps = DesiredCapabilities().CHROME
        caps["pageLoadStrategy"] = "eager"

        if ENV == "server":
            driver = webdriver.Chrome(
                'chromedriver',
                desired_capabilities=caps,
                options=chrome_options
            )
        else:
            driver = webdriver.Chrome(
                desired_capabilities=caps,
                executable_path=ChromeDriverManager().install(),
                options=chrome_options
            )
        return driver
    except:
        print("Init failed, trying again")
        return None


def login(driver):
    try:
        WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, modal_close_xpath))).click()
    except:
        pass
    print("Passed modal")

    WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, signin_enter_xpath))).click()
    WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, username_input_xpath)))
    driver.find_element(By.XPATH, username_input_xpath).send_keys(USERNAME)
    driver.find_element(By.XPATH, password_input_xpath).send_keys(PASSWORD)
    driver.find_element(By.XPATH, signin_button_xpath).click()
    return driver


def setup():
    for i in range(5):
        try:
            driver = init_driver()
            driver.get(BASE_URL)
            print(f'Visiting {driver.title}')
            driver = login(driver)
            return driver
        except:
            print("Setup failed, trying again")
            continue
        break


def get_links(driver):
    driver.get(LISTING_URL)
    print(f'Visiting {driver.title}')
    try:
        element = driver.find_elements(By.XPATH, list_names_xpath)
        element = [el.get_attribute('href') for el in element]
    except:
        print("No links found")
        element = []
    return element


def get_details(driver, links):
    for link in links[:10]:
        for i in range(5):
            try:
                driver.get(f'{link}-historical-data')
                WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, open_daterange_xpath)))
                driver.find_element(By.XPATH, open_daterange_xpath).click()
                driver.find_element(By.XPATH, start_date_input_xpath).clear()
                start_date = last_year(20).strftime("%m/%d/%Y")
                driver.find_element(By.XPATH, start_date_input_xpath).send_keys(start_date)
                driver.find_element(By.XPATH, apply_button_xpath).click()
                WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, price_table_first_row_xpath)))
                print("Downloading csv")
                driver.find_element(By.XPATH, download_button_xpath).click()
                print(driver.find_element(By.XPATH, fund_title_xpath).text)
            except:
                print("Failed to get details, trying again")
                driver = setup()
                continue
            break


def exec():
    print("Scraping Investing.com Fund Data")
    driver = setup()

    print("Getting Links")
    links = get_links(driver)
    print(len(links))

    print("Getting Details")
    get_details(driver, links)

    print('Closing Driver')
    driver.close()
    driver.quit()


if __name__ == '__main__':
    exec()
