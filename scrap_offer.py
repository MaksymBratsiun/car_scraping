import datetime
import os
import platform

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait


TITLE_XPATH = '/html//h1'
PRICE_XPATH = '/html//div[@class="price_value"]'
PRICE_ADD_XPATH = '/html//div[@class="price_value price_value--additional"]'
ODOMETER_XPATH = '/html//div[@class="base-information bold"]'
IMG_COUNT_XPATH = '/html//div[@class="action_disp_all_block"]'
IMG_XPATH = '/html//div[@class="photo-620x465 loaded"]'
PHONE_XPATH = '/html//span[@class="phone bold"]'
PHONE_CONV_XPATH = '/html//span[@class="conversion_phone_newcars"]'
VIN_CODE_XPATH = '/html//span[@class="vin-code"]'
VIN_LABEL_XPATH = '/html//span[@class="label-vin"]'
NUMBER_XPATH = '/html//span[@class="state-num ua"]'
SELLER_NAME_DIV_XPATH = '/html//div[@class="seller_info_name bold"]'
SELLER_NAME_H4_XPATH = '/html//h4[@class="seller_info_name"]'


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
    price_usd = 0
    try:
        div_element = driver.find_element(By.XPATH, PRICE_XPATH).text
        if '$' in div_element:
            price_usd = int(div_element.split('$')[0].replace(' ', ''))
        else:
            div_element = driver.find_element(By.XPATH, PRICE_ADD_XPATH).text
            div_element = div_element.split('•')
            for element in div_element:
                if "$" in element:
                    price_usd = element.split('$')[0].replace(' ', '')
    except Exception as e:
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
    div_element = '0 тис'
    try:
        div_element = driver.find_element(By.XPATH, ODOMETER_XPATH).text
    except Exception as e:
        print('Failure odometer')
    try:
        odometer = div_element.split('тис')[0].replace(' ', '')
    except Exception as e:
        odometer = 0
    if odometer.isalpha():
        odometer = 0
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
        div_element = driver.find_element(By.XPATH, IMG_COUNT_XPATH).text
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
        div_element = driver.find_element(By.XPATH, IMG_XPATH)
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
    The scrap_phone function takes a driver as an argument and returns the phone number of the restaurant.
        The function first tries to find the popup element that contains the phone number, then clicks on it.
        If successful, it will return a string containing only digits (no spaces or dashes). Otherwise, None is returned.

    :param driver: Access the web page
    :return: The phone number of the restaurant
    :doc-author: Trelent
    """
    phone = None
    try:
        popup = driver.find_element(By.XPATH, PHONE_XPATH)
        driver.execute_script("arguments[0].click();", popup)
        webdriver.ActionChains(driver).move_to_element(popup).click(popup).perform()
        phone = popup.text
    except Exception as e:
        print('Failute phone')
    if not phone:
        try:
            popup = driver.find_element(By.XPATH, PHONE_CONV_XPATH)
            driver.execute_script("arguments[0].click();", popup)
            webdriver.ActionChains(driver).move_to_element(popup).click(popup).perform()
            phone = popup.text
        except Exception as e:
            phone = 'without phone'
            print('Failute phone')
    return phone


def scrap_vin(driver):
    """
    The scrap_vin function scrapes the VIN code from a given car's webpage.
        Args:
            driver (selenium webdriver): The selenium webdriver object that is used to scrape the page.

    :param driver: Access the web page
    :return: The vin code of the car
    :doc-author: Trelent
    """

    vin = None
    try:
        vin = driver.find_element(By.XPATH, VIN_CODE_XPATH).text
    except Exception as e:
        print('Failure vin-code')
    if not vin:
        try:
            vin = driver.find_element(By.XPATH, VIN_LABEL_XPATH).text
        except Exception as e:
            print('Failure vin-label')
            vin = 'without vin'
    return vin


def scrap_number(driver):
    """
    The scrap_number function takes in a driver object and returns the number of the restaurant.
      If there is no number, it will return &quot;no number&quot;.

    :param driver: Pass the driver object to the function
    :return: The number of the restaurant
    :doc-author: Trelent
    """
    try:

      number = driver.find_element(By.XPATH, NUMBER_XPATH).text
    except Exception as e:
        number = "no number"
    return number


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
        div_element = driver.find_element(By.XPATH, SELLER_NAME_DIV_XPATH).text
    except Exception as e:
        div_element = 'Can`t scrap'
        print('Failure individual username')
    if div_element == 'Can`t scrap':
        try:
            div_element = driver.find_element(By.XPATH, SELLER_NAME_H4_XPATH).text
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
        title = driver.find_element(By.XPATH, TITLE_XPATH).text.strip()
        price_usd = scrap_price(driver)
        odometer = scrap_odometer(driver)
        username = scrap_username(driver)
        image_url = scrap_image(driver)
        images_count = scrap_img_count(driver)
        car_vin = scrap_vin(driver)
        car_number = scrap_number(driver)
        phone_number = scrap_phone(driver)
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
