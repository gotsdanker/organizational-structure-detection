from manufacturing_company.src.common.Const import *
import numpy as np
import pandas as pd


def remove_former_employee_and_technical_accounts(communication, reportsto):
    reportsto_processed = reportsto[reportsto[REPORTS_TO_ID].str.isnumeric()]
    reportsto_processed[REPORTS_TO_ID] = pd.to_numeric(reportsto_processed[REPORTS_TO_ID])

    senders = reportsto_processed[ID]
    recipients = reportsto_processed[REPORTS_TO_ID]
    employees = np.hstack([senders, recipients])
    employees = np.unique(employees)

    communication_processed = communication[communication[SENDER].isin(employees) & communication[RECIPIENT].isin(employees)]

    return communication_processed, reportsto_processed