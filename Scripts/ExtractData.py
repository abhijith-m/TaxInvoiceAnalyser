import sys
import re
from Utils.fileHandler import *
from db_helper import dbHandler as dB
from datetime import datetime

def extract_data(pdf_file):
    if not check_file_exists(pdf_file):
        raise Exception(f'File: {pdf_file} not found')
    pdf_path = get_files_directory() + pdf_file
    csv_path = extract_pdf_to_csv(pdf_path)

    row_count = 0
    rows_to_be_inserted = []
    for row in read_csv(csv_path):
        val_row = validate_entry(row)
        if val_row:
            rows_to_be_inserted.append(val_row)
            row_count += 1
            if row_count % 20 == 0:
                # Do a batch insert
                dB.insert_entry(rows_to_be_inserted)
                rows_to_be_inserted = []
            # dB.insert_entry(val_row)
    if rows_to_be_inserted:
        dB.insert_entry(rows_to_be_inserted)
    print(f'{row_count} rows inserted.')

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

            max_borrower_name_len = get_max_borrower_len()
            if not desc and len(borrower) >= max_borrower_name_len:
                desc = borrower[max_borrower_name_len:]
                borrower = borrower[:max_borrower_name_len]

            max_sub_broker_len = get_max_sub_broker_len()
            if not borrower and len(sub_broker) >= max_sub_broker_len:
                borrower = sub_broker[max_sub_broker_len:]
                sub_broker = sub_broker[:max_sub_broker_len]

            return tuple([app_id, xref, setl_date, broker, sub_broker, borrower, desc, tot_loan_amt,
                          comm, upfront, upfront_gst])

        except BaseException as e:
            print(f"Error parsing row: {entry}, \n Exception: {e.args}")
            return None
    return None

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

