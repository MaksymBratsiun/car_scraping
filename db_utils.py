import os
import datetime

from dotenv import load_dotenv

from connect_db import session
from models import Offers


load_dotenv()

DUMP_DIR = 'dumps'

username = os.environ.get('POSTGRES_USER')
password = os.environ.get('POSTGRES_PASSWORD')
port = os.environ.get('POSTGRES_PORT')
host = os.environ.get('POSTGRES_HOST')
db_name = os.environ.get('POSTGRES_DB_NAME')
container = os.environ.get('POSTGRES_CONTAINER')


def make_dump():
    """
    The make_dump function creates a backup of the database.
        It first tries to create a dump using docker, and if that fails it will try to create one locally.


    :return: None
    :doc-author: Trelent
    """
    backup_file_name = f"backup_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.sql"
    backup_file_path = os.path.join(os.getcwd(), DUMP_DIR, backup_file_name)
    error_flag = False
    try:
        command = f"docker exec -i {container} pg_dump -U {username} " \
                  f"-h {host} -p {port} -F c -b -v -d {db_name} > {backup_file_path}"
        os.system(command)
    except Exception as e:
        error_flag = True
        print(f"failure docker dump: {e}")

    if error_flag:
        try:
            command = f"pg_dump -U {username} -h {host} -p {port} -F c -b -v -f {backup_file_path} {db_name}"
            os.system(command)

        except Exception as e:
            print(f"failure local postgresql dump: {e}")


def add_to_db(data):
    """
    The add_to_db function takes a dictionary as an argument and adds it to the database.

    :param data: Pass the data from the scrap_offer() function to this one
    :return: None
    :doc-author: Trelent
    """
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


def add_all_to_db(data_list):
    offers_list = []
    for data in data_list:
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
        offers_list.append(offer)
    session.add_all(offers_list)
    session.commit()


def get_previous_urls():
    """
    The get_previous_urls function returns a list of all the URLs that have been scraped in the past.
    This is used to prevent duplicate entries from being added to the database.

    :return: A list of all the urls that have been scraped previously
    :doc-author: Trelent
    """
    res_query = session.query(Offers.url).select_from(Offers).all()
    result = [i[0] for i in res_query]
    return result
