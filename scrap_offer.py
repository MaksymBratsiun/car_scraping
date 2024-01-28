import datetime
import os
import platform

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait


def path_driver():
    """
    The path_driver function returns the path to the chromedriver executable.
    It is a helper function for other functions in this module.


    :return: The path of the driver that will be used to run the tests
    :doc-author: Trelent
    """
    if platform.system() == 'Windows':
        res = os.path.join(os.getcwd(), 'drivers', 'chromedriver_win32', 'chromedriver.exe')
    elif platform.system() == 'Linux':
        res = os.path.join(os.getcwd(), 'drivers', 'chromedriver_linux64', 'chromedriver.exe')
    else:
        res = None
    return res


def scrap_price(driver):
    """
    The scrap_price function takes a driver as an argument and returns the price of the item in USD.
        The function first finds the div element with class &quot;price_value&quot; and then splits it by '$'
        to get only the number part of it. Then, we replace all spaces with nothing ('') so that we can convert
        this string into an int.

    :param driver: Pass the webdriver object to the function
    :return: The price of the product in usd
    :doc-author: Trelent
    """
    div_element = driver.find_element(By.XPATH, '/html//div[@class="price_value"]').text
    try:
        price_usd = int(div_element.split('$')[0].replace(' ', ''))
    except Exception as e:
        price_usd = 0
        print('Failure price')

    return price_usd


def scrap_odometer(driver):
    """
    The scrap_odometer function takes a driver as an argument and returns the odometer value of the car.
        The function first tries to find a div element with class 'base-information bold' and then splits it by 'тис'.
        If there is no such element, it returns 0. Otherwise, it removes all spaces from the string and converts
        it into integer.

    :param driver: Get the current page source
    :return: The odometer value in kilometers
    :doc-author: Trelent
    """
    try:
        div_element = driver.find_element(By.XPATH, '/html//div[@class="base-information bold"]').text
    except Exception as e:
        div_element = '0 тис'
        print('Failure odometer')
    odometer = div_element.split('тис')[0].replace(' ', '')
    return int(odometer)*1000


def scrap_img_count(driver):
    """
    The scrap_img_count function takes in a driver object and returns the number of images on the page.
        It does this by finding an element with class 'action_disp_all_block' and then splitting its text into a list,
        where the third item is always going to be an integer representing how many images are on that page.

    :param driver: Pass the webdriver object to the function
    :return: The number of images in the page
    :doc-author: Trelent
    """
    try:
        div_element = driver.find_element(By.XPATH, '/html//div[@class="action_disp_all_block"]').text
    except Exception as e:
        div_element = '0'
        print('Failure img count')
    count_img = div_element.strip().split(' ')
    if len(div_element) >= 3:
        count_img = int(count_img[2])
    else:
        count_img = 0
    return count_img


def scrap_image(driver):
    """
    The scrap_image function takes in a driver object and returns the src value of an image.
        If there is no image, it will return 'without url' or 'video without url'.


    :param driver: Get the current page of the browser
    :return: The url of the image, if there is an image
    :doc-author: Trelent
    """
    try:
        div_element = driver.find_element(By.XPATH, '/html//div[@class="photo-620x465 loaded"]')
        img_element = div_element.find_element(By.XPATH, './/img')
        src_value = img_element.get_attribute('src')
    except Exception as e:
        print('Failure img')
        src_value = None

    if not src_value:
        try:
            div_element = driver.find_element(By.XPATH, '/html//div[@class="video-stories"]')
            if div_element:
                src_value = 'video without url'
            else:
                src_value = 'without url'
        except Exception as e:
            print('failure img')
            src_value = 'without url'

    return src_value


def scrap_phone(driver):
    """
    The scrap_phone function takes in a driver object and returns the phone number of the business.
        Args:
            driver (object): A Selenium webdriver object.

    :param driver: Pass the driver object to the function
    :return: The phone number of the business
    :doc-author: Trelent
    """

    phone_element = driver.find_element(By.XPATH, '/html//span[@class="mhide"]').text
    return phone_element


def scrap_vin_number(driver):
    """
    The scrap_vin_number function scrapes the vin number and state number from a car's page.
        Args:
            driver (selenium webdriver): The selenium webdriver object that is used to scrape the data.

    :param driver: Find the elements in the html code
    :return: A tuple, which is a list of two elements: vin and number
    :doc-author: Trelent
    """
    try:
        vin = driver.find_element(By.XPATH, '/html//span[@class="vin-code"]').text
    except Exception as e:
        print('Failure vin')
        vin = None

    if not vin:
        try:
            vin = driver.find_element(By.XPATH, '/html//span[@class="label-vin"]').text
        except Exception as e:
            print('Failure vin')
            vin = 'without vin'

    try:
        number = driver.find_element(By.XPATH, '/html//span[@class="state-num ua"]').text
    except Exception as e:
        number = "no number"
    return vin, number


def scrap_username(driver):
    """
    The scrap_username function scrapes the username of the seller from a given webpage.
        It first tries to find an element with class &quot;seller_info_name bold&quot; and if it fails,
        it tries to find an element with class &quot;seller_info_name&quot;. If both fail, then we return
        'Can`t scrap' as a string.

    :param driver: Get the username of the seller
    :return: The username of the seller
    :doc-author: Trelent
    """
    try:
        div_element = driver.find_element(By.XPATH, '/html//div[@class="seller_info_name bold"]').text
    except Exception as e:
        div_element = 'Can`t scrap'
        print('Failure individual username')
    if div_element == 'Can`t scrap':
        try:
            div_element = driver.find_element(By.XPATH, '/html//h4[@class="seller_info_name"]').text
        except Exception as e:
            div_element = 'Can`t scrap'
            print('Failure company username')

    username = div_element.strip()
    return username


def scrap_offer(target_url):
    """
    The scrap_offer function scrapes the target_url for the following information:
        - title
        - price in USD
        - odometer reading in km (kilometers)
        - username of seller
        - phone_number
        - image_url
        - images_count
        - car_vin
        - car_number
        - datetime_found (date)


    :param target_url: Pass the url of the offer to be scraped
    :return: A dictionary with the following keys:
    :doc-author: Trelent
    """
    service = Service(path_driver())
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
    # datetime_found = datetime.date.today() - datetime.timedelta(days=1)

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
