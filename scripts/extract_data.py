import sys
import re
import settings
from utils.file_handler import *
from utils import constants
from db_helper import db_handler as db
from datetime import datetime
from itertools import islice

def extract_data(pdf_file):
    if not check_file_exists(pdf_file):
        raise Exception(f'File: {pdf_file} not found')
    pdf_path = get_files_directory() + pdf_file
    csv_path = extract_pdf_to_csv(pdf_path)

    transactions = []
    for row in read_csv(csv_path):
        val_row = validate_entry(row)
        if val_row:
            transactions.append(val_row)

    transaction_count = 0
    if transactions:
        transaction_count = insert_transactions(transactions)

    print(f'{transaction_count} rows inserted.')

def validate_entry(entry: list[str]):
    row_pattern = \
        r"^(\d+) (\d+) (\d+/\d+/\d+) ([A-Za-z'\- ]+) ([\d,]+\.\d{2}) (\d+\.\d{2}) ([\d,]+\.\d{2}) ([\d,]+\.\d{2})$"
    match = re.match(row_pattern, ' '.join(entry))
    if match:
        try:
            app_id = int(entry[0].strip())
            xref = int(entry[1].strip())
            setl_date = get_date(entry[2])
            broker = entry[3].strip()
            sub_broker = entry[4].strip() if entry[4] else None
            borrower = entry[5].strip()
            desc = entry[6].strip()
            tot_loan_amt = get_numeric_value(entry[7])
            comm = get_numeric_value(entry[8])
            upfront = get_numeric_value(entry[9])
            upfront_gst = get_numeric_value(entry[10])

            max_borrower_name_len = constants.MAX_BORROWER_LEN
            if not desc and len(borrower) >= max_borrower_name_len:
                desc = borrower[max_borrower_name_len:]
                borrower = borrower[:max_borrower_name_len]

            max_sub_broker_len = constants.MAX_SUB_BROKER_LEN
            if not borrower and len(sub_broker) >= max_sub_broker_len:
                borrower = sub_broker[max_sub_broker_len:]
                sub_broker = sub_broker[:max_sub_broker_len]

            return tuple([app_id, xref, setl_date, broker, sub_broker, borrower, desc, tot_loan_amt,
                          comm, upfront, upfront_gst])

        except BaseException as e:
            print(f"Error parsing row: {entry}, \n Exception: {e.args}")
            return None
    return None

def insert_transactions(transactions):
    transaction_count = 0
    for transaction_batch in batch_transactions(transactions):
        transaction_count += db.insert_entry(transaction_batch)
    return transaction_count

def batch_transactions(transactions):
    chunk = constants.TRANSACTION_BATCH_SIZE
    transaction_iter = iter(transactions)
    while transaction_batch := list(islice(transaction_iter, chunk)):
        yield transaction_batch

def get_date(val: str):
    return datetime.strptime(val.strip(), '%d/%m/%Y').date()

def get_numeric_value(val: str) -> float:
    return float(val.strip().replace(',', '').replace(' ', ''))


if __name__ == '__main__':
    filename = 'Test PDF.pdf'
    if len(sys.argv) > 1:
        filename = sys.argv[1]
    create_files_directory(os.getcwd())
    extract_data(filename)

