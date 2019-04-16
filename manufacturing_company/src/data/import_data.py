import pandas as pd


def load_communication():
    return pd.read_csv('manufacturing_company/data/raw/communication.csv', sep=';', parse_dates=True)


def load_reportsto():
    return pd.read_csv('manufacturing_company/data/raw/reportsto.csv', sep=';')

