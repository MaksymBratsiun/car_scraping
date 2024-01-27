import os
import platform
from datetime import date, timedelta

from connect_db import session
from models import Offers


from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec

from scrap_offer import scrap_offer

load_dotenv()

URL = os.environ.get('SITE_URL')
PAGE = 3

# URL = "https://auto.ria.com/uk/auto_ford_ecosport_35940791.html"
# URL = "https://auto.ria.com/uk/auto_bmw_x6_35935575.html"
# URL = "https://auto.ria.com/uk/auto_nissan_tiida_35841097.html"


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


def get_previous_urls():
    previous_day = date.today() - timedelta(days=1)
    res_query = session.query(Offers.url).select_from(Offers).where(Offers.datetime_found == previous_day).all()
    result = [i[0] for i in res_query]
    return result


def add_to_db(data):
    offer = Offers(
        url=data.get('url'),
        title=data.get('title'),
        price_usd=data.get('price_usd'),
        odometer=data.get('odometer'),
        username=data.get('username'),
        phone_number=data.get('phone_number'),
        image_url=data.get('image_url'),
        images_count=data.get('images_count'),
        car_number=data.get('car_number'),
        car_vin=data.get('car_vin'),
        datetime_found=data.get('datetime_found')
        )
    session.add(offer)
    session.commit()


if __name__ == '__main__':
    target_url = f'{URL}/?page={PAGE}'
    previous_urls = get_previous_urls()
    for url in scrap_site(target_url):
        if url not in previous_urls:
            add_to_db(scrap_offer(url))
        else:
            print('duplicate found')
            break
    # for i, v in scrap_offer(URL).items():
    #     print(i, ': ', v)
    #

