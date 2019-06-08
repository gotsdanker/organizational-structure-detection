import numpy as np
import pandas as pd

from manufacturing_company.src.common.const import *


def remove_former_employee_and_technical_accounts(communication, reportsto):
    reportsto = reportsto[reportsto[REPORTS_TO_ID].str.isnumeric()].copy()
    reportsto[REPORTS_TO_ID] = pd.to_numeric(reportsto[REPORTS_TO_ID])

    communication = communication[communication[SENDER].isin(reportsto[ID]) & communication[RECIPIENT].isin(reportsto[ID])].copy()

    return communication, reportsto


def remove_messages_sent_to_yourself(communication, reportsto):
    communication = communication[communication[SENDER] != communication[RECIPIENT]].copy()

    reportsto = reportsto[reportsto[ID].isin(communication[SENDER]) | reportsto[ID].isin(communication[RECIPIENT])].copy()

    return communication, reportsto
