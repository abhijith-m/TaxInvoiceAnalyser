import sys
from db_helper.dbHandler import *

def get_highest_loan_amt_by_broker(broker_name: str):
    try:
        high_loan_amt, = get_highest_loan_broker(broker_name)
        print(f'')

    except:
        pass


if __name__ == '__main__':
    if len(sys.argv) < 2:
        raise Exception(f'please specify broker name')
    broker_name = sys.argv[1]
