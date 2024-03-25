MAX_SUB_BROKER_LEN = 21

MAX_BORROWER_LEN = 31

TRANSACTION_BATCH_SIZE = 20

CREATE_TABLE_TRANSACTION = ("CREATE TABLE IF NOT EXISTS INVOICE_TRANSACTION ("
                            "app_id int NOT NULL, "
                            "xref int NOT NULL, "
                            "settlement_date date NOT NULL, "
                            "broker_name varchar(50) NOT NULL, "
                            "sub_broker_name varchar(50), "
                            "borrower_name varchar(50) NOT NULL, "
                            "description varchar(30) NOT NULL, "
                            "total_loan_amt NUMERIC(1000, 2) NOT NULL, "
                            "commission_rate NUMERIC(3, 2) NOT NULL, "
                            "upfront NUMERIC(1000, 2) NOT NULL, "
                            "upfront_incl_gst NUMERIC(1000, 2) NOT NULL, "
                            "UNIQUE(xref, total_loan_amt) "
                            ");")

DATE_WISE_LOAN_INDEX = ("CREATE UNIQUE INDEX IF NOT EXISTS date_wise_loan_amt "
                        "ON INVOICE_TRANSACTION (settlement_date, xref, total_loan_amt);")

BROKER_WISE_LOAN_INDEX = ("CREATE UNIQUE INDEX IF NOT EXISTS broker_wise_loan_amt "
                          "ON INVOICE_TRANSACTION (broker_name, xref, total_loan_amt);")

INSERT_ENTRY = "INSERT INTO INVOICE_TRANSACTION VALUES {} ON CONFLICT (xref, total_loan_amt) DO NOTHING;"

TOT_LOAN_AMT = ("SELECT sum(total_loan_amt) FROM INVOICE_TRANSACTION "
                "WHERE settlement_date >= %s and settlement_date <= %s;")

HIGHEST_LOAN_BY_BROKER = ("SELECT total_loan_amt FROM INVOICE_TRANSACTION "
                          "WHERE broker_name = %s ORDER BY total_loan_amt DESC LIMIT 1; ")

LOANS_BY_BROKER = ("SELECT settlement_date, total_loan_amt FROM INVOICE_TRANSACTION "
                   "WHERE broker_name = %s ORDER BY settlement_date ASC, total_loan_amt DESC;")

GROUP_LOANS_BY_DATE = ("SELECT settlement_date, SUM(total_loan_amt) FROM INVOICE_TRANSACTION "
                       "GROUP BY settlement_date;")

TIER_1_LOANS_COUNT = ("SELECT settlement_date, COUNT(total_loan_amt) FROM INVOICE_TRANSACTION "
                      "WHERE total_loan_amt > 100000 GROUP BY settlement_date;")

TIER_2_LOANS_COUNT = ("SELECT settlement_date, COUNT(total_loan_amt) FROM INVOICE_TRANSACTION "
                      "WHERE total_loan_amt > 50000 and total_loan_amt < 100000 GROUP BY settlement_date;")

TIER_3_LOANS_COUNT = ("SELECT settlement_date, COUNT(total_loan_amt) FROM INVOICE_TRANSACTION "
                      "WHERE total_loan_amt > 10000 and total_loan_amt < 50000 GROUP BY settlement_date;")
