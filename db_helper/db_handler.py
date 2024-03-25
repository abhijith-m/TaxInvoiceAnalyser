import os
import psycopg2
import logging
from utils import constants

logging.basicConfig(filename=os.getcwd() + '/logs/record.log', level=logging.INFO)
logger = logging.getLogger()

def insert_entry(entry):
    try:
        with psycopg2.connect(Db.CONNECTION_STRING) as conn:
            with conn.cursor() as cursor:
                entry_list = ','.join(['%s'] * len(entry))

                # print(constants.INSERT_ENTRY.format(entry_list))
                # print(cursor.mogrify(constants.INSERT_ENTRY.format(entry_list), entry).decode('utf8'))

                cursor.execute(constants.INSERT_ENTRY.format(entry_list), entry)
                return cursor.rowcount
    except psycopg2.Error as e:
        logger.error(e)
        print(e)
        raise e

def get_loan_amount(st_date, end_date):
    try:
        with psycopg2.connect(Db.CONNECTION_STRING) as conn:
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
        with psycopg2.connect(Db.CONNECTION_STRING) as conn:
            with conn.cursor() as cursor:
                cursor.execute(constants.HIGHEST_LOAN_BY_BROKER, (broker_name,))
                row = cursor.fetchone()
                return row
    except psycopg2.Error as e:
        logger.error(e)
        print(e)
        raise e

def get_loan_by_broker(broker_name):
    try:
        with psycopg2.connect(Db.CONNECTION_STRING) as conn:
            with conn.cursor() as cursor:
                cursor.execute(constants.LOANS_BY_BROKER, (broker_name,))
                rows = cursor.fetchall()
                return rows
    except psycopg2.Error as e:
        logger.error(e)
        print(e)
        raise e

def get_total_loan_group_by_date():
    try:
        with psycopg2.connect(Db.CONNECTION_STRING) as conn:
            with conn.cursor() as cursor:
                cursor.execute(constants.GROUP_LOANS_BY_DATE)
                rows = cursor.fetchall()
                return rows
    except psycopg2.Error as e:
        logger.error(e)
        print(e)
        raise e

def get_tier_1_loan_group_by_date():
    try:
        with psycopg2.connect(Db.CONNECTION_STRING) as conn:
            with conn.cursor() as cursor:
                cursor.execute(constants.TIER_1_LOANS_COUNT)
                rows = cursor.fetchall()
                return rows
    except psycopg2.Error as e:
        logger.error(e)
        print(e)
        raise e

def get_tier_2_loan_group_by_date():
    try:
        with psycopg2.connect(Db.CONNECTION_STRING) as conn:
            with conn.cursor() as cursor:
                cursor.execute(constants.TIER_2_LOANS_COUNT)
                rows = cursor.fetchall()
                return rows
    except psycopg2.Error as e:
        logger.error(e)
        print(e)
        raise e

def get_tier_3_loan_group_by_date():
    try:
        with psycopg2.connect(Db.CONNECTION_STRING) as conn:
            with conn.cursor() as cursor:
                cursor.execute(constants.TIER_3_LOANS_COUNT)
                rows = cursor.fetchall()
                return rows
    except psycopg2.Error as e:
        logger.error(e)
        print(e)
        raise e

class Db:
    CONNECTION_STRING = None

    def __init__(self, url):
        logger.info("Creating database table")
        Db.CONNECTION_STRING = url
        Db.create_tables()
        logger.info("Created database table")

    @staticmethod
    def create_tables():
        try:
            with psycopg2.connect(Db.CONNECTION_STRING) as conn:
                with conn.cursor() as cursor:
                    cursor.execute(constants.CREATE_TABLE_TRANSACTION)
                    cursor.execute(constants.DATE_WISE_LOAN_INDEX)
                    cursor.execute(constants.BROKER_WISE_LOAN_INDEX)
        except psycopg2.InterfaceError as e:
            logger.error(f'Error while creating table {e}')

