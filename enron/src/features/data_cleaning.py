import datetime
import pandas as pd

from enron.src.common.const import *
from manufacturing_company.src.common.const import *


def delete_nan(employees, emails):
    employees = employees.dropna(axis=0, subset=[POSITION])
    employee_ids = employees.index
    emails = emails[emails[SENDER].isin(employee_ids) & emails[RECIPIENT].isin(employee_ids)]
    return employees.copy(), emails.copy()


def group_duplicates_email_addresses(employees):
    employees = employees.reset_index()
    return employees.groupby([NAME, POSITION, DETAILS])[ID].apply(list)


def remap_employee_ids(employees, emails):
    grouped_employees = group_duplicates_email_addresses(employees)

    id_map = {}

    def create_map_with_new_ids(row):
        more_than_one_id = len(row) > 1

        if more_than_one_id:
            first_id = row[0]
            other_ids = row[1:]

            id_map[first_id] = other_ids

    grouped_employees.apply(create_map_with_new_ids)

    # remap other ids to the first id
    new_ids = {k: oldk for oldk, oldv in id_map.items() for k in oldv}

    return emails.replace(new_ids)


def delete_messages_sent_to_yourself(emails):
    return emails[emails[SENDER] != emails[RECIPIENT]].copy()


def delete_messages_with_boundary_dates(emails):
    after_enron_creation = emails[EVENT_DATE] >= pd.Timestamp(datetime.date(1985, 8, 1))
    before_enron_liquidation = emails[EVENT_DATE] < pd.Timestamp(datetime.date(2001, 12, 1))
    return emails[after_enron_creation & before_enron_liquidation].copy()
