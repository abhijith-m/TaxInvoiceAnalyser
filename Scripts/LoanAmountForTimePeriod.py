import sys
from db_helper.dbHandler import *
from datetime import datetime

def get_loan_amt_for_time_range(start_date, end_date):
    try:
        start_date = datetime.strptime(start_date, '%d/%m/%Y').date()
        end_date = datetime.strptime(end_date, '%d/%m/%Y').date()
        if start_date <= end_date:
            raise Exception(f'Start date should be less than End date.')
        loan_amt, = get_loan_amount(start_date, end_date)
        print(f"Total loan amount from {start_date} to {end_date} : {loan_amt} ")
    except Exception as e:
        print(e)
        raise e


if __name__ == '__main__':
    if len(sys.argv) < 2:
        raise Exception(f'Specify start date and end date')
    get_loan_amt_for_time_range(sys.argv[1], sys.argv[2])
