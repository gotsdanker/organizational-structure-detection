import numpy as np
import pandas as pd

from manufacturing_company.src.common.const import *


def remove_former_employee_and_technical_accounts(communication, reportsto):
    reportsto = reportsto[reportsto[REPORTS_TO_ID].str.isnumeric()].copy()
    reportsto[REPORTS_TO_ID] = pd.to_numeric(reportsto[REPORTS_TO_ID])

    communication = __intersect(reportsto, communication, ID, SENDER, REPORTS_TO_ID, RECIPIENT)

    return communication, reportsto


def remove_messges_sent_to_yourself(communication, reportsto):
    communication = communication[communication[SENDER] != communication[RECIPIENT]]

    reportsto = __intersect(communication, reportsto, SENDER, ID, RECIPIENT, REPORTS_TO_ID)

    return communication, reportsto


def __intersect(employees1, employees2, sender_label_1, sender_label_2, recipient_label_1, recipient_label_2):
    senders = employees1[sender_label_1]
    recipients = employees1[recipient_label_1]
    employees = np.hstack([senders, recipients])
    employees = np.unique(employees)

    return employees2[employees2[sender_label_2].isin(employees) & employees2[recipient_label_2].isin(employees)]