import os
import psycopg2
import logging
from Utils import constants

logging.basicConfig(filename=os.getcwd() + '/Logs/record.log', level=logging.INFO)
logger = logging.getLogger()

def insert_entry(entry):
    try:
        with psycopg2.connect(Db.URL) as conn:
            with conn.cursor() as cursor:
                entry_list = ','.join(['%s'] * len(entry))

                # print(constants.INSERT_ENTRY.format(entry_list))
                # print(cursor.mogrify(constants.INSERT_ENTRY.format(entry_list), entry).decode('utf8'))

                cursor.execute(constants.INSERT_ENTRY.format(entry_list), entry)
                row = cursor.rowcount
                return row
    except psycopg2.Error as e:
        logger.error(e)
        print(e)
        raise e

def get_loan_amount(st_date, end_date):
    try:
        with psycopg2.connect(Db.URL) as conn:
            with conn.cursor() as cursor:
                cursor.execute(constants.TOT_LOAN_AMT, (st_date, end_date))
                row = cursor.fetchone()
                return row
    except psycopg2.Error as e:
        logger.error(e)
        print(e)
        raise e

def get_highest_loan_broker(broker_name):
    try:
        with psycopg2.connect(Db.URL) as conn:
            with conn.cursor() as cursor:
                cursor.execute(constants.HIGHEST_LOAN_BY_BROKER, (broker_name,))
                row = cursor.fetchone()
                return row
    except psycopg2.Error as e:
        logger.error(e)
        print(e)
        raise e

class Db:
    URL = None

    def __init__(self, url):
        logger.info("Initialising db tables")
        Db.URL = url

        self.create_tables()
        logger.info("Initialised db tables")

    def create_tables(self):
        try:
            with psycopg2.connect(Db.URL) as conn:
                with conn.cursor() as cursor:
                    cursor.execute(constants.CREATE_TABLE_TRANSACTION)
        except psycopg2.InterfaceError as e:
            logger.error(f'Error while creating table Transaction: {e}')

