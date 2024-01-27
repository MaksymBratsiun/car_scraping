import os
import platform

from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec

from scrap_offer import scrap_offer

load_dotenv()

# URL = os.environ.get('SITE_URL')
# PAGE = 1

# URL = "https://auto.ria.com/uk/auto_ford_ecosport_35940791.html"
# URL = "https://auto.ria.com/uk/auto_bmw_x6_35935575.html"
URL = "https://auto.ria.com/uk/auto_volkswagen_id_4_crozz_35939765.html"


def scrap_site(input_url):
    offers = []

    if platform.system() == 'Windows':
        path_driver = os.path.join(os.getcwd(), 'drivers', 'chromedriver_win32', 'chromedriver.exe')
    elif platform.system() == 'Linux':
        path_driver = os.path.join(os.getcwd(), 'drivers', 'chromedriver_linux64', 'chromedriver.exe')
    else:
        path_driver = None

    service = Service(path_driver)
    options = webdriver.ChromeOptions()
    options.add_argument('--headless=chrome')

    with webdriver.Chrome(service=service, options=options) as driver:
        driver.get(input_url)
        WebDriverWait(driver, 10)
        urls = driver.find_elements(By.XPATH, '/html//a[@class ="m-link-ticket"]')
        for link in urls:
            offers.append(link.get_attribute('href'))

    return offers


if __name__ == '__main__':
    # target_url = f'{URL}/?page={PAGE}'
    # for url in scrap_site(target_url):
    #     print(scrap_offer(url))
    for i, v in scrap_offer(URL).items():
        print(i, ': ', v)










