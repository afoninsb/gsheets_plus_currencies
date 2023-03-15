from sqlalchemy import Column, Date, Float, Integer, create_engine
from sqlalchemy.orm import DeclarativeBase

import os
from dotenv import load_dotenv

load_dotenv()


class Base(DeclarativeBase):
    pass


class Order(Base):
    __tablename__ = 'api_order'

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    number = Column(Integer, index=True)
    price_usd = Column(Integer)
    price_rub = Column(Float)
    delivery_day = Column(Date)


database = (f'postgresql://{os.getenv("POSTGRES_USER")}:'
            f'{os.getenv("POSTGRES_PASSWORD")}@{os.getenv("DB_HOST")}/'
            f'{os.getenv("POSTGRES_DB")}')
engine = create_engine(database)
