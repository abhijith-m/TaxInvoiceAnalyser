import os
from dotenv import load_dotenv
from db_helper.dbHandler import Db

load_dotenv()

Db(os.getenv("DATABASE_URL"))
# Db(os.getenv("LOCAL_DB"))
API_KEY = os.getenv("API_KEY")
MAX_SUB_BROKER_LEN = int(os.getenv("MAX_SUB_BROKER_LEN"))
MAX_BORROWER_LEN = int(os.getenv("MAX_BORROWER_LEN"))

def get_api_key():
    return API_KEY

def get_max_sub_broker_len():
    return MAX_SUB_BROKER_LEN

def get_max_borrower_len():
    return MAX_BORROWER_LEN

