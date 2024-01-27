import os
from datetime import date, timedelta

from connect_db import session
from models import Offers

from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait

from scrap_offer import scrap_offer, path_driver

load_dotenv()

URL = os.environ.get('SITE_URL')
START_PAGE = os.environ.get('START_PAGE')
END_PAGE = os.environ.get('END_PAGE')


def scrap_page(input_url):
    offers = []

    service = Service(path_driver())
    options = webdriver.ChromeOptions()
    options.add_argument('--headless=chrome')

    with webdriver.Chrome(service=service, options=options) as driver:
        driver.get(input_url)
        WebDriverWait(driver, 10)
        urls = driver.find_elements(By.XPATH, '/html//a[@class ="m-link-ticket"]')
        for link in urls:
            offers.append(link.get_attribute('href'))
    return offers


def scrap_site(site_url=URL, start_page=START_PAGE, end_page=END_PAGE):
    count_page = start_page
    previous_urls = get_previous_urls()
    exit_flag = False
    while previous_page_exists(count_page):
        if END_PAGE and count_page > end_page:
            print('end page found -', end_page)
            break
        target_url = f'{site_url}/?page={count_page}'
        for url in scrap_page(target_url):
            print('page', count_page, 'url', url)
            if url not in previous_urls:
                add_to_db(scrap_offer(url))
            else:
                print('duplicate found')
                exit_flag = True
                break
        if exit_flag:
            break
        count_page += 1


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


def previous_page_exists(input_page):
    input_url = f'{URL}/?page={input_page}'
    service = Service(path_driver())
    options = webdriver.ChromeOptions()
    options.add_argument('--headless=chrome')

    with webdriver.Chrome(service=service, options=options) as driver:
        driver.get(input_url)
        WebDriverWait(driver, 5)
        try:
            res = driver.find_element(By.XPATH, '/html//a[@class ="page-link js-next "]')
            print('next page exists')
            result = True
        except Exception as e:
            print('next page not exists')
            result = False
    return result


if __name__ == '__main__':
    scrap_site()
