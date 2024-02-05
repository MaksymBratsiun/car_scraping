import os
import time

import schedule
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait

from scrap_offer import scrap_offer, path_driver
from db_utils import add_to_db, get_previous_urls, make_dump

load_dotenv()

URL = os.environ.get('SITE_URL')
START_PAGE = int(os.environ.get('START_PAGE'))
END_PAGE = int(os.environ.get('END_PAGE'))
ACTIVATE_TIME = os.environ.get('ACTIVATE_TIME')


def scrap_page(input_url):
    """
    The scrap_page function takes in an url and returns a list of urls for each offer on the page.
        Args:
            input_url (str): The url to be scraped.

    :param input_url: Get the url of the page we want to scrap
    :return: A list of urls
    :doc-author: Trelent
    """
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


def scrap_site(site_url, start_page=1, end_page=None):
    """
    The scrap_site function scrapes the site for all offers.
    It takes three arguments:
        - site_url (str): The url of the website to be scraped.
        - start_page (int): The page number from which scraping should begin. Default is 1, i.e., first page of results
        on the website's search engine; if None, it will scrape from first page onwards until no more pages are found or
         end_page is reached; if a positive integer n &gt; 1, it will scrape starting with that specific result page
         and continue until no more pages are found or end_page is reached; if a

    :param site_url: Specify the site to be scraped
    :param start_page: Set the page number from which we start scraping
    :param end_page: Set the maximum number of pages to be scraped
    :return: None
    :doc-author: Trelent
    """
    count_page = start_page
    previous_urls = get_previous_urls()
    while next_page_exists(count_page):
        if END_PAGE and count_page > end_page:
            print('end page found -', end_page)
            break
        target_url = f'{site_url}/?page={count_page}'
        for url in scrap_page(target_url):
            print('page', count_page, 'url', url)
            if url not in previous_urls:
                add_to_db(scrap_offer(url))
        count_page += 1


def next_page_exists(input_page):
    """
    The next_page_exists function takes in a page number and returns True if there is a next page, False otherwise.
    It does this by checking for the existence of an element with class 'page-link js-next' on the input_url.

    :param input_page: Determine the page number of the url
    :return: True if there is a next page, false otherwise
    :doc-author: Trelent
    """
    input_url = f'{URL}/?page={input_page}'
    service = Service(path_driver())
    options = webdriver.ChromeOptions()
    options.add_argument('--headless=chrome')

    with webdriver.Chrome(service=service, options=options) as driver:
        driver.get(input_url)
        WebDriverWait(driver, 3)
        try:
            result = bool(driver.find_element(By.XPATH, '/html//a[@class ="page-link js-next "]'))
            print('next page exists')
        except Exception as e:
            print('next page not exists')
            result = False
    return result


def main():
    """
    The main function scrapes the site and creates a dump of the data.


    :return: None
    :doc-author: Trelent
    """
    make_dump()
    scrap_site(site_url=URL, start_page=START_PAGE, end_page=END_PAGE)


if __name__ == '__main__':
    time_start = time.time()
    print("Start common")
    scrap_site(site_url=URL, start_page=1, end_page=2)
    print("time common: ", time.time() - time_start)

    # schedule.every().day.at(ACTIVATE_TIME).do(main)
    # while True:
    #     schedule.run_pending()
    #     time.sleep(10)
