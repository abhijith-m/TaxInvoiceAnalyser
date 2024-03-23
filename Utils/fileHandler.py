import os
from pathlib import Path
from settings import *
import pdftables_api
import csv

def create_files_directory(dir_path):
    try:
        if not os.path.exists(dir_path + '/Files'):
            os.mkdir(dir_path+'/Files')
        return True
    except BaseException as e:
        raise f'Exception: {e}'

def get_files_directory():
    # par_dir = os.path.abspath(os.path.join(os.getcwd(), os.pardir))
    file_dir = os.getcwd() + '/Files/'
    if os.path.exists(file_dir):
        return file_dir
    return None

def check_file_exists(filename):
    # par_dir = os.path.abspath(os.path.join(os.getcwd(), os.pardir))
    file_dir = os.getcwd() + '/Files/'
    file = Path(file_dir + filename)
    print(file_dir)
    return file.is_file()

def extract_pdf_to_csv(pdf_path):
    path = Path(pdf_path)
    # par_dir = os.path.abspath(os.path.join(os.getcwd(), os.pardir))
    file_dir = os.getcwd()
    csv_path = file_dir + '/Files/' + path.stem + '.csv'

    if Path(csv_path).exists():
        os.remove(csv_path)

    pdf_client = pdftables_api.Client(get_api_key())
    try:
        pdf_client.csv(pdf_path, csv_path)

    except BaseException as e:
        raise f'Exception Occurred!{e}, {e.args}'
    return csv_path

def clean_up_csv(csv_path):
    with open(csv_path, 'r') as file:
        csv_reader = csv.reader(file)
        for line in csv_reader:
            pass

def read_csv(csv_path):
    with open(csv_path, 'r') as file:
        csv_reader = csv.reader(file)
        for line in csv_reader:
            yield line
