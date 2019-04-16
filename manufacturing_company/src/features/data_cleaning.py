from manufacturing_company.src.common.const import *
import numpy as np
import pandas as pd


def remove_former_employee_and_technical_accounts(communication, reportsto):
    reportsto_processed = reportsto[reportsto[REPORTS_TO_ID].str.isnumeric()]
    reportsto_processed[REPORTS_TO_ID] = pd.to_numeric(reportsto_processed[REPORTS_TO_ID])

    communication_processed = __intersect(reportsto_processed, communication, ID, SENDER, REPORTS_TO_ID, RECIPIENT)

    return communication_processed, reportsto_processed


def remove_messges_sent_to_yourself(communication, reportsto):
    communication_processed = communication[communication[SENDER] != communication[RECIPIENT]]

    reportsto_processed = __intersect(communication_processed, reportsto, SENDER, ID, RECIPIENT, REPORTS_TO_ID)

    return communication_processed, reportsto_processed


def __intersect(employees1, employees2, sender_label_1, sender_label_2, recipient_label_1, recipient_label_2):
    senders = employees1[sender_label_1]
    recipients = employees1[recipient_label_1]
    employees = np.hstack([senders, recipients])
    employees = np.unique(employees)

    return employees2[employees2[sender_label_2].isin(employees) & employees2[recipient_label_2].isin(employees)]