from manufacturing_company.src.common.const import *
from enron.src.common.const import *
import pandas as pd


def load_employees():
    employees = pd.read_csv('enron/data/raw/employees.txt', sep=';', header=None)
    employees.index.name = ID
    employees.columns = [EMAIL, NAME, POSITION, DETAILS]
    return employees


def load_emails():
    emails = pd.read_csv('enron/data/raw/execs.email.linesnum', sep=' ')
    emails.columns = [EVENT_DATE, SENDER, RECIPIENT]
    emails[EVENT_DATE] = pd.to_datetime(emails[EVENT_DATE], unit='s')
    return emails
