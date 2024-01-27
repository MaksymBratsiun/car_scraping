import datetime
import os
import platform


from bs4 import BeautifulSoup
import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec

from scrap_offer import scrap_offer

URL_NEXT = "https://auto.ria.com/uk/car/used/?page=2"
URL_USED = "https://auto.ria.com/uk/car/used/"

URL = "https://auto.ria.com/uk/auto_bmw_x5_35920151.html"
# URL = "https://auto.ria.com/uk/auto_bmw_x6_35935575.html"


if __name__ == '__main__':
    for i, v in scrap_offer(URL).items():
        print(i, ': ', v)
    # if platform.system() == 'Windows':
    #     path_driver = os.path.join(os.getcwd(), 'drivers', 'chromedriver_win32', 'chromedriver.exe')
    # elif platform.system() == 'Linux':
    #     path_driver = os.path.join(os.getcwd(), 'drivers', 'chromedriver_linux64', 'chromedriver.exe')
    # else:
    #     path_driver = None
    #
    # service = Service(path_driver)
    # options = webdriver.ChromeOptions()
    # options.add_argument('--headless=chrome')
    #
    # with webdriver.Chrome(service=service, options=options) as driver:
    #     driver.get(URL_USED)
    #     WebDriverWait(driver, 3)
    #     res = driver.find_elements(By.XPATH, '/html//a[@class ="m-link-ticket"]')
        # for link in res:
        #     print(link.get_attribute("href"))









