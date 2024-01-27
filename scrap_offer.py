import datetime
import os
import platform


from bs4 import BeautifulSoup
import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait


def scrap_price(driver):
    try:
        div_element = driver.find_element(By.XPATH, '/html//div[@class="price_value"]').text
    except Exception as e:
        div_element = '0$'
        print('Failure price')
    price_usd = div_element.split('$')[0].replace(' ', '')
    return int(price_usd)


def scrap_odometer(driver):
    try:
        div_element = driver.find_element(By.XPATH, '/html//div[@class="base-information bold"]').text
    except Exception as e:
        div_element = '0 тис'
        print('Failure odometer')
    odometer = div_element.split('тис')[0].replace(' ', '')
    return int(odometer)*1000


#TODO
def scrap_img_count(driver):
    try:
        div_element = driver.find_element(By.XPATH, '/html//div[@class="action_disp_all_block"]').text
    except Exception as e:
        div_element = '0 0 0 0'
        print('Failure img count')
    count_img = div_element.strip().split(' ')
    return int(count_img[2])


def scrap_image(driver):
    div_element = driver.find_element(By.XPATH, '/html//div[@class="photo-620x465 loaded"]')
    img_element = div_element.find_element(By.XPATH, './/img')
    src_value = img_element.get_attribute('src')
    return src_value


#TODO
def scrap_phone(driver):
    phone_element = driver.find_element(By.XPATH, '/html//span[@class="mhide"]').text
    return phone_element


#TODO
def scrap_vin_number(driver):
    try:
        vin = driver.find_element(By.XPATH, '/html//span[@class="vin-code"]').text
    except Exception as e:
        print('Failure vin')
        vin = driver.find_element(By.XPATH, '/html//span[@class="label-vin"]').text

    try:
        number = driver.find_element(By.XPATH, '/html//span[@class="state-num ua"]').text
    except Exception as e:
        number = "no number"

    return vin, number


def scrap_username(driver):
    try:
        div_element = driver.find_element(By.XPATH, '/html//div[@class="seller_info_name bold"]').text
    except Exception as e:
        div_element = 'Can`t scrap'
        print('Failure individual username')

    try:
        div_element = driver.find_element(By.XPATH, '/html//h4[@class="seller_info_name"]').text
    except Exception as e:
        div_element = 'Can`t scrap'
        print('Failure company username')

    username = div_element.strip()
    return username


def scrap_offer(target_url):
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
        driver.get(target_url)
        WebDriverWait(driver, 3)
        title = driver.find_element(By.XPATH, '/html//h1[@class="head"]').text.strip()
        price_usd = scrap_price(driver)
        odometer = scrap_odometer(driver)
        username = scrap_username(driver)
        phone_number = scrap_phone(driver)
        image_url = scrap_image(driver)
        images_count = scrap_img_count(driver)
        car_vin, car_number = scrap_vin_number(driver)
    datetime_found = datetime.date.today()

    return {
        'url': target_url,
        'title': title,
        'price_usd': price_usd,
        'odometer': odometer,
        'username': username,
        'phone_number': phone_number,
        'image_url': image_url,
        'images_count': images_count,
        'car_number': car_number,
        'car_vin': car_vin,
        'datetime_found': datetime_found
        }
