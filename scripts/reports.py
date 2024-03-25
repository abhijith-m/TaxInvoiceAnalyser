import settings
from db_helper.db_handler import *
from datetime import datetime


def get_highest_loan_amt_by_broker(broker_name: str):
    try:
        result = get_highest_loan_broker(broker_name)
        if not result:
            print(f"Broker with name: {broker_name} doesn't have any loans\n")
            return
        high_loan_amt, = result
        print(f"\nHighest loan amount of Broker with name: {broker_name} = {high_loan_amt}\n")
    except BaseException as e:
        raise e

def get_loan_amt_for_time_range(start_date, end_date):
    try:
        start_date = datetime.strptime(start_date, '%d/%m/%Y').date()
        end_date = datetime.strptime(end_date, '%d/%m/%Y').date()
        if start_date > end_date:
            raise Exception(f'Start date should be less than or equal to End date.\n')

        result = get_loan_amount(start_date, end_date)
        loan_amt = result[0] if result else 0

        print(f"\nTotal loan amount from {start_date} to {end_date} : {loan_amt} \n")
    except BaseException as e:
        print(e)
        raise e

def get_datewise_loan_amt_for_broker(broker_name):
    try:
        result = get_loan_by_broker(broker_name)
        if result:
            display_datewise_loan(result)
        else:
            print(f'\nNo loan exists for broker: {broker_name}.\n')
    except BaseException as e:
        raise e

def total_loans_by_date():
    try:
        result = get_total_loan_group_by_date()
        if result:
            display_datewise_loan(result)
        else:
            print(f'\nNo loan exists.\n')
    except BaseException as e:
        raise e


def display_datewise_loan(date_wise_loan):
    date_fmt, loan_fmt = '{arg:}'.center(14), '{arg:}'.center(12)
    settlement_dates = set()
    print('-' * 40)
    print('Settlement Date'.center(20) + '\t' + 'Loan Amount'.center(15))

    for date, loan_amt in date_wise_loan:
        if date in settlement_dates:
            print(date_fmt.format(arg=' '*10) + '\t' + loan_fmt.format(arg=loan_amt))
        else:
            print('-' * 40)
            print(date_fmt.format(arg=str(date.strftime("%d/%m/%Y"))) + '\t' + loan_fmt.format(arg=loan_amt))
            settlement_dates.add(date)
    print('-' * 40)

def tier_wise_group_loan_amt():
    try:
        tier_1_loans = get_tier_1_loan_group_by_date()
        if tier_1_loans:
            print('\nTier 1 Loan amount grouped by date.')
            display_datewise_loan(tier_1_loans)
        tier_2_loans = get_tier_2_loan_group_by_date()
        if tier_2_loans:
            print('\nTier 2 Loan amount grouped by date.')
            display_datewise_loan(tier_2_loans)
        tier_3_loans = get_tier_3_loan_group_by_date()
        if tier_3_loans:
            print('\nTier 3 Loan amount grouped by date.')
            display_datewise_loan(tier_3_loans)

    except BaseException as e:
        raise e


if __name__ == "__main__":
    print('Tax Invoice Report generation')
    print('Select from the below options')
    print('\t 1. Get total loan amount for a given date range. \n'
          '\t 2. Get highest loan amount for a broker. \n'
          '\t 3. Get date-wise report of loan amounts for a broker. \n'
          '\t 4. Get a report of total loan amount by date. \n'
          '\t 5. Get date-wise report of number of loans under each tier. \n')

    inp = int(input('Input your option: ').strip())
    match inp:
        case 1:
            print('\nPlease enter date range in format DD/MM/YYYY')
            st_date = input('Start Date: ').strip()
            end_date = input('End Date: ').strip()
            get_loan_amt_for_time_range(st_date, end_date)

        case 2:
            print('\nHighest loan amount given by a broker:')
            broker_name = input('Enter Broker name: ').strip()
            get_highest_loan_amt_by_broker(broker_name)

        case 3:
            print("\nDate-wise report of loan amounts for a broker:")
            broker_name = input('Enter Broker name: ').strip()
            get_datewise_loan_amt_for_broker(broker_name)

        case 4:
            print("\nTotal loan amounts grouped by date:")
            total_loans_by_date()

        case 5:
            print('\nTier-wise total loan amounts:')
            tier_wise_group_loan_amt()

        case _:
            print('\nPlease select valid input. Exiting.')
