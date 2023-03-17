import logging
import os
import xml.etree.ElementTree as ET
from datetime import datetime
from http import HTTPStatus
from pathlib import Path
from time import sleep
from typing import List, Union

import db
import gspread
import requests
from dotenv import load_dotenv
from execptions import SaveXMLError
from gspread.exceptions import APIError, GSpreadException
from lxml import etree
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

load_dotenv()


def get_exchange_rates(file_path: str) -> None:
    """Получаем xml-файл с курсами валют и сохраняем его."""

    response = requests.get(os.getenv('EXCHANGE_XML'))
    try:
        with open(file_path, 'w') as file:
            file.write(response.text)
    except Exception as err:
        raise SaveXMLError(
            f'Не удалось сохранить xml-файл: {err}'
        ) from err


def exhange_rate(file_path: str) -> float:
    """Получаем текущий курс из xml-файла."""

    parser = etree.XMLParser(recover=True)
    try:
        tree = ET.parse(file_path, parser=parser)
    except FileNotFoundError as err:
        raise FileNotFoundError('Нет xml-файла с курсами валют') from err
    return float(tree.find('Valute[@ID="R01235"]')[4].text.replace(',', '.'))


def get_gs_data(path: str) -> List[List[Union[str, int]]] | None:
    """Получаем информацию из Гугл-таблицы."""

    path = f'{path}/.conf/{os.getenv("GOOGLE_API_KEY")}'
    try:
        gc = gspread.service_account(filename=path)
    except FileNotFoundError as err:
        raise FileNotFoundError('Нет файла в приватным ключем Google') from err
    SPREADSHEET_KEY = str(os.getenv('SPREADSHEET_KEY'))
    try:
        spreadsheet = gc.open_by_key(SPREADSHEET_KEY)
    except APIError as err:
        raise APIError('Неверный ключ таблицы Google') from err
    worksheet = spreadsheet.sheet1
    try:
        return worksheet.get_all_values()
    except GSpreadException as err:
        raise GSpreadException(
            'Ошибка получения данных с Гугл Таблицы: {err}'
        ) from err


def is_overdue(order_date: str, number: int) -> None:
    """Проверяем сроки заказа."""

    today = datetime.now().strftime('%Y.%m.%d')
    dt = order_date.split('.')
    order_date = f'{dt[2]}.{dt[1]}.{dt[0]}'
    if order_date < today:
        send_message(number)


def transform_data(
    data: List[List[Union[str, int]]], exchange: float
) -> list[db.Order]:
    """Преобразуем информацию из Гугл-таблицы в формат,
    удобный для сохранения в базу данных."""

    db_data = [1] * (len(data) - 1)
    for count, row in enumerate(data):
        if count == 0:
            continue
        delivery_day = row[3]
        number = int(row[1])
        price_usd = int(row[2])
        price_rub = round(price_usd * exchange, 2)
        db_data[count-1] = db.Order(
            number=number,
            price_usd=price_usd,
            price_rub=price_rub,
            delivery_day=delivery_day
        )
        # Если заказ просрочен, отправляем сообщение в бот
        is_overdue(delivery_day, number)
    return db_data


def data_to_db(data: List[db.Order]) -> None:
    """Сохраняем информацию в базу данных."""

    try:
        with Session(autoflush=False, bind=db.engine) as session:
            session.query(db.Order).delete()
            session.commit()
            session.add_all(data)
            session.commit()
    except SQLAlchemyError as err:
        raise SQLAlchemyError(
            f'Ошибка при сохранении в базу данных: {err}'
        ) from err


def send_message(number: int) -> None:
    """Отправляем сообщения в бот."""

    url = f'https://api.telegram.org/bot{os.getenv("TOKEN")}/sendMessage'
    text = f'Просрочен заказ номер {number}'
    message = {
        'chat_id': os.getenv('CHAT_ID'),
        'text': text,
    }
    send = requests.post(url, data=message)
    if send.status_code != HTTPStatus.OK:
        logging.warning(f'Ошибка отправки сообщения: {text}')


def create_dir(path):
    """Создаём папку для рабочих файлов."""

    path = f'{path}/received_files'
    if not os.path.exists(path):
        os.makedirs(path)


if __name__ == '__main__':
    logging.basicConfig(
        level=logging.INFO,
        filename='log_error.log',
        filemode='w',
        format='[%(asctime)s] %(levelname).1s %(message)s',
        datefmt='%Y.%m.%d %H:%M:%S',
    )
    path = Path(__file__).resolve().parent
    create_dir(path)
    file_path = f'{path}/received_files/currencies.xml'
    while True:
        try:
            get_exchange_rates(file_path)
            exchange = exhange_rate(file_path)
            data = get_gs_data(path)
            data = transform_data(data, exchange)
            data_to_db(data)
        except (
            SaveXMLError,
            SQLAlchemyError,
            GSpreadException,
            APIError,
            FileNotFoundError,
            Exception
        ) as err:
            logging.error(err)
        sleep(int(os.getenv('CRON_TIME')) * 3600)
