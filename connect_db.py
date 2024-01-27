import os
from dotenv import load_dotenv
from sqlalchemy.engine import create_engine
from sqlalchemy.orm import sessionmaker

load_dotenv()

username = os.environ.get('POSTGRES_USER')
password = os.environ.get('POSTGRES_PASSWORD')
port = os.environ.get('POSTGRES_PORT')
host = os.environ.get('POSTGRES_HOST')
db_name = os.environ.get('POSTGRES_DB_NAME')


url_to_db = f'postgresql+psycopg2://{username}:{password}@{host}:{port}/{db_name}'

engine = create_engine(url_to_db, echo=False, pool_size=5)
Session = sessionmaker(bind=engine)
session = Session()
