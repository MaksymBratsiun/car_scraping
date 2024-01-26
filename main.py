import os
import datetime

from dotenv import load_dotenv
import requests
from bs4 import BeautifulSoup

URL = "https://auto.ria.com/uk/auto_bmw_x5_35920151.html"

load_dotenv()

username = os.environ.get("LOGIN_USERNAME")
password = os.environ.get("LOGIN_PASSWORD")

login_url = 'https://auto.ria.com/uk/login'
login_payload = {
    'username': username,
    'password': password
    }

if __name__ == '__main__':
    with requests.Session() as session:
        login_request = session.post(login_url, data=login_payload)

        if login_request.status_code == 200:

            target_url = 'https://auto.ria.com/uk/auto_bmw_x6_35935575.html'

            response = session.get(target_url)
            soup = BeautifulSoup(response.text, 'lxml')
            url = target_url
            title = soup.find('h1', class_='head').text
            price_usd = soup.find('div', class_='price_value').text
            odometer = soup.find('div', class_='base-information bold').text
            username_ = soup.find('div', class_='seller_info_name bold').text
            phone_number = soup.find('div', class_='phones_item').text  # need selenium
            image_url = soup.find('div', class_='photo-620x465 loaded')  # need selenium
            images_count = soup.find('span', class_='count').text
            car_number = soup.find('span', class_='state-num ua')  # need selenium
            car_vin = soup.find('span', class_='vin-code').text
            datetime_found = datetime.date.today()

        else:
            print('Login failed. Status code:', login_request.status_code)
    print(url)
    print(title)
    print(price_usd)
    print(odometer)
    print(username_)
    print(phone_number, "number")
    print(image_url)
    print(images_count)
    print(car_number)
    print(car_vin)
    print(datetime_found)
