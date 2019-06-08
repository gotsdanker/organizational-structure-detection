import pandas as pd
from manufacturing_company.src.common.const import *


SATURDAY = 5
SUNDAY = 6


def remove_employees_below_minimum_activity(communication, months):
    while True:
        communication_frequency = communication.drop_duplicates([SENDER, YEAR, MONTH]).groupby(SENDER).count()

        employees_under_threshold = communication_frequency[communication_frequency[MONTH] < months].index

        # drop employees who never sent or received an email
        at_least_one_message_sent = communication[RECIPIENT].isin(communication[SENDER])
        at_least_one_message_received = communication[SENDER].isin(communication[RECIPIENT])
        at_least_one_message_sent_and_received = at_least_one_message_sent & at_least_one_message_received

        if (len(communication[~at_least_one_message_sent_and_received]) > 0) | (len(employees_under_threshold) != 0):
            sender_above_threshold = ~communication[SENDER].isin(employees_under_threshold)
            recipient_above_threshold = ~communication[RECIPIENT].isin(employees_under_threshold)
            criteria = at_least_one_message_sent_and_received & sender_above_threshold & recipient_above_threshold
            communication = communication[criteria]
        else:
            break

    return communication


def calculate_overtime(df, from_hour, to_hour):
    df[OVERTIME] = 0
    overtime_selector = (((df[EVENT_DATE].dt.hour >= from_hour) & (df[EVENT_DATE].dt.hour <= 23)) | (
                (df[EVENT_DATE].dt.hour >= 0) & (df[EVENT_DATE].dt.hour <= to_hour))) & \
                        (df[EVENT_DATE].dt.weekday != SATURDAY) & (df[EVENT_DATE].dt.weekday != SUNDAY)
    df.loc[overtime_selector, OVERTIME] = 1
    df_overtime = df[[SENDER, OVERTIME]].groupby(SENDER).sum()
    return pd.DataFrame(df_overtime, columns=[OVERTIME])


def calculate_work_at_weekend(df):
    df[WORK_AT_WEEKEND] = 0
    weekend_selector = (df[EVENT_DATE].dt.weekday == SATURDAY) | (df[EVENT_DATE].dt.weekday == SUNDAY)
    df.loc[weekend_selector, WORK_AT_WEEKEND] = 1
    df_weekend = df[[SENDER, WORK_AT_WEEKEND]].groupby(SENDER).sum()
    return pd.DataFrame(df_weekend, columns=[WORK_AT_WEEKEND])
