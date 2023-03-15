from time import sleep
from typing import List, Union
import gspread
import os
from dotenv import load_dotenv
from gspread.exceptions import GSpreadException
from pathlib import Path
import requests
from sqlalchemy.orm import Session
import xml.etree.ElementTree as ET
from lxml import etree
import db

load_dotenv()


def get_exchange_rates(file_path: str) -> None:
    response = requests.get(os.getenv('EXCHANGE_XML'))
    with open(file_path, 'w') as file:
        file.write(response.text)


def exhange_rate(file_path: str) -> float:
    parser = etree.XMLParser(recover=True)
    tree = ET.parse(file_path, parser=parser)
    return float(tree.find('Valute[@ID="R01235"]')[4].text.replace(',', '.'))


def get_gs_data(path: str) -> List[List[Union[str, int]]] | None:
    path = f'{path}/.config/{os.getenv("GOOGLE_API_KEY")}'
    gc = gspread.service_account(filename=path)
    SPREADSHEET_KEY = str(os.getenv('SPREADSHEET_KEY'))
    spreadsheet = gc.open_by_key(SPREADSHEET_KEY)
    worksheet = spreadsheet.sheet1
    try:
        return worksheet.get_all_values()
    except GSpreadException:
        print('Ошибка получения данных с Гугл Таблицы')


def gs_data_to_db(data: List[List[Union[str, int]]], exchange: float) -> None:
    db_data = [1] * (len(data) - 1)
    for count, row in enumerate(data):
        if count == 0:
            continue
        price_usd = int(row[2])
        price_rub = round(price_usd * exchange, 2)
        db_data[count-1] = db.Order(
            number=int(row[1]),
            price_usd=price_usd,
            price_rub=price_rub,
            delivery_day=row[3]
        )
    with Session(autoflush=False, bind=db.engine) as session:
        session.query(db.Order).delete()
        session.commit()
        session.add_all(db_data)
        session.commit()


def import_data():
    while True:
        path = Path(__file__).resolve().parent
        file_path = f'{path}/.config/data.xml'
        get_exchange_rates(file_path)
        exchange = exhange_rate(file_path)
        data = get_gs_data(path)
        gs_data_to_db(data, exchange)
        sleep(int(os.getenv('CRON_TIME')) * 3600)


if __name__ == '__main__':
    import_data()
