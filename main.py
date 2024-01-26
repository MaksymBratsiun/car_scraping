import datetime
import os
import platform


from bs4 import BeautifulSoup
from dotenv import load_dotenv
import requests
from selenium import webdriver

from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec


URL_USED = "https://auto.ria.com/uk/car/used/"
URL = "https://auto.ria.com/uk/auto_bmw_x5_35920151.html"
# URL = "https://auto.ria.com/uk/auto_bmw_x6_35935575.html"

load_dotenv()

username = os.environ.get("LOGIN_USERNAME")
password = os.environ.get("LOGIN_PASSWORD")

login_url = 'https://auto.ria.com/uk/login'
login_payload = {
    'username': username,
    'password': password
    }


def scrap_data(target_url):
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
        image_url = scrap_image(driver, target_url)
        phone_number = scrap_phone(driver, target_url)
        car_number = scrap_car_number(driver, target_url)
        car_vin = scrap_vin(driver, target_url)


    response = requests.get(target_url)
    soup = BeautifulSoup(response.text, 'lxml')

    title = soup.find('h1', class_='head').text.strip()
    price_usd = processed_price(soup.find('div', class_='price_value').text)
    odometer = processed_odometer(soup.find('div', class_='base-information bold').text)
    username_ = soup.find('div', class_='seller_info_name bold').text.strip()
    images_count = processed_img_count(soup.find('div', class_='action_disp_all_block').text)
    # images_count = processed_img_count(soup.find('span', class_='count').text)
    # car_vin = soup.find('span', class_='vin-code').text  # need selenium
    # car_vin_1 = soup.find('span', class_='label-vin')  # need selenium
    datetime_found = datetime.date.today()

    return {
        'url': target_url,
        'title': title,
        'price_usd': price_usd,
        'odometer': odometer,
        'username': username_,
        'phone_number': phone_number,
        'image_url': image_url,
        'images_count': images_count,
        'car_number': car_number,
        'car_vin': car_vin,
        'datetime_found': datetime_found
        }


def processed_price(input_price):
    res = input_price.split('$')[0].replace(' ', '')
    return int(res)


def processed_odometer(input_odometer):
    res = input_odometer.split('тис')[0].replace(' ', '')
    return int(res)*1000


#TODO
def processed_img_count(input_count):
    count_img = input_count.strip().split(' ')
    return int(count_img[2])


def scrap_image(driver, target_url):

    driver.get(target_url)
    div_element = driver.find_element(By.XPATH, '/html//div[@class="photo-620x465 loaded"]')
    img_element = div_element.find_element(By.XPATH, './/img')
    src_value = img_element.get_attribute('src')
    return src_value


#TODO
def scrap_phone(driver, target_url):
    driver.get(target_url)
    phone_element = driver.find_element(By.XPATH, '/html//span[@class="mhide"]').text
    return phone_element


#TODO
def scrap_car_number(driver, target_url):

    driver.get(target_url)

    # div_element = driver.find_element(By.XPATH, '/html//span[@class="state-num ua"]')
    # res = div_element.text
    return "Cannot scrap"


#TODO
def scrap_vin(driver, target_url):

    driver.get(target_url)

    try:
        vin = driver.find_element(By.XPATH, '/html//span[@class="vin-code"]').text
    except:
        vin_element = driver.find_element(By.XPATH, '/html//span[@class="label-vin"]').text
        vin = vin_element
    return vin


if __name__ == '__main__':
    # for i, v in scrap_data(URL).items():
    #     print(i, ': ', v)
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
        driver.get(URL_USED)
        WebDriverWait(driver, 3)
        res = driver.find_elements(By.XPATH, '/html//a[@class ="m-link-ticket"]')
        # for link in res:
        #     print(link.get_attribute("href"))
        








