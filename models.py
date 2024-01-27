from sqlalchemy import Column, Integer, String, Date
from sqlalchemy.orm import declarative_base

from connect_db import engine


Base = declarative_base()


class Offers(Base):
    __tablename__ = "offers"
    id = Column(Integer, primary_key=True)
    url = Column(String(255), nullable=False, unique=True)
    title = Column(String(255), nullable=False)
    price_usd = Column(Integer)
    odometer = Column(Integer)
    username = Column(String(63))
    phone_number = Column(String(31), nullable=False)
    image_url = Column(String(255))
    images_count = Column(Integer)
    car_number = Column(String(12))
    car_vin = Column(String(17))
    datetime_found = Column(Date, nullable=False)


Base.metadata.create_all(engine)
