import os
from dotenv import load_dotenv
from db_helper.db_handler import Db

load_dotenv()

Db(os.getenv("DATABASE_URL"))
# Db(os.getenv("LOCAL_DB"))
API_KEY = os.getenv("API_KEY")

def get_api_key():
    return API_KEY


