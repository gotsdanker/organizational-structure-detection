import pandas as pd
from manufacturing_company.src.common.const import *


def load_communication():
    return pd.read_csv('manufacturing_company/data/raw/communication.csv', sep=';', parse_dates=[EVENT_DATE])


def load_reportsto():
    return pd.read_csv('manufacturing_company/data/raw/reportsto.csv', sep=';')

