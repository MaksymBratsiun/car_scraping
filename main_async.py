import os
import time
from concurrent.futures import ThreadPoolExecutor

import asyncio
import schedule
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait


from scrap_offer import scrap_offer, path_driver
from db_utils import add_all_to_db, get_previous_urls, make_dump

load_dotenv()

URL = os.environ.get('SITE_URL')
START_PAGE = int(os.environ.get('START_PAGE'))
END_PAGE = int(os.environ.get('END_PAGE'))
ACTIVATE_TIME = os.environ.get('ACTIVATE_TIME')
THREADS = 10


def scrap_page(input_url):

    """
    The scrap_page function takes in a url and returns a list of urls for each offer on the page.
        Args:
            input_url (str): The url to be scraped.

    :param input_url: Pass the url to the function
    :return: A list of links to offers
    :doc-author: Trelent
    """
    offers = []
    service = Service(path_driver())
    options = webdriver.ChromeOptions()
    options.add_argument('--headless=chrome')

    with webdriver.Chrome(service=service, options=options) as driver:
        driver.get(input_url)
        WebDriverWait(driver, 1)
        urls = driver.find_elements(By.XPATH, '/html//a[@class ="m-link-ticket"]')
        for link in urls:
            offers.append(link.get_attribute('href'))
    return offers


def next_page_exists(input_page):
    """
    The previous_page_exists function takes in a page number and returns True if the previous page exists,
        False otherwise.
        It does this by checking for the existence of an element with class 'page-link js-next' on the input_url.
        If it finds that element, it returns True; if not, it returns False.

    :param input_page: Navigate to the page that we want to check if it exists or not
    :return: True if the next page exists and false if it does not
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
            flag = bool(driver.find_element(By.XPATH, '/html//a[@class ="page-link js-next "]'))
            print('next page exists')
        except Exception as e:
            print('next page not exists')
            flag = False
    return flag


def page_fetch(input_url):
    """
    The page_fetch function takes in a URL and returns the HTML of that page.
        It is used to fetch the HTML of a given page, which can then be parsed by BeautifulSoup.

    :param input_url: Pass the url to the function
    :return: A dictionary with the following keys:
    :doc-author: Trelent
    """
    res_ = scrap_offer(input_url)
    return res_


def scrap_site(site_url, start_page=1, end_page=None):

    """
    The scrap_site function scrapes the site for all pages, starting from start_page and ending at end_page.
    It uses the scrap_page function to scrape each page, and then adds all of the urls in that page to a list.
    If there are any urls in that list which have not been previously added to our database (as determined by
    the get_previous_urls function), it will add them asynchronously using asyncio.

    :param site_url: Specify the site that we want to scrap
    :param start_page: Set the page number to start scraping from
    :param end_page: Specify the last page to be scraped
    :return: A list of dictionaries
    :doc-author: Trelent
    """
    count_page = start_page
    previous_urls = get_previous_urls()
    while next_page_exists(count_page):
        if END_PAGE and count_page > end_page:
            print('end page found -', end_page)
            break
        target_url = f'{site_url}/?page={count_page}'
        urls_in_page = scrap_page(target_url)
        to_work = [item for item in urls_in_page if item not in previous_urls]  # find unique urls in

        result = asyncio.run(async_main(to_work))
        add_all_to_db(result)

        count_page += 1


async def async_main(urls):

    """
    The async_main function takes a list of urls and returns the html content for each url.
        It uses asyncio to run the page_fetch function in parallel, using 3 threads.

        Args:
            urls (list): A list of strings representing URLs to fetch HTML from.

    :param urls: Pass in the list of urls to be fetched
    :return: A coroutine object
    :doc-author: Trelent
    """
    loop = asyncio.get_running_loop()
    with ThreadPoolExecutor(THREADS) as pool:
        futures = [loop.run_in_executor(pool, page_fetch, url) for url in urls]
        result_ = await asyncio.gather(*futures)
        return result_


def main():
    """
    The main function scrapes the site and creates a dump of the data.


    :return: None
    :doc-author: Trelent
    """
    make_dump()
    scrap_site(site_url=URL, start_page=START_PAGE, end_page=END_PAGE)


if __name__ == "__main__":
    # time_start = time.time()
    # print("Start async")
    # scrap_site(site_url=URL, start_page=1, end_page=2)
    # print("time async: ", time.time() - time_start)

    schedule.every().day.at(ACTIVATE_TIME).do(main)
    while True:
        schedule.run_pending()
        time.sleep(10)
