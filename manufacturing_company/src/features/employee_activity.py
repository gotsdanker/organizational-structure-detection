from manufacturing_company.src.common.const import *
import pandas as pd


def remove_employees_below_minimum_activity(communication, months):
    end = False

    while not end:
        communication_frequency = communication.groupby(SENDER)[MONTH].nunique().sort_values()

        employees_under_threshold = communication_frequency[communication_frequency < months].index

        if len(employees_under_threshold) != 0:
            criteria = (~communication[SENDER].isin(employees_under_threshold)) & (~communication[RECIPIENT].isin(employees_under_threshold))
            communication = communication[criteria]
        else:
            end = True

    return communication


def calculate_overtime(df, from_hour, to_hour):
    df[OVERTIME] = 0
    overtime_selector = ((df[EVENT_DATE].dt.hour >= from_hour) & (df[EVENT_DATE].dt.hour <= 23)) | (
                (df[EVENT_DATE].dt.hour >= 0) & (df[EVENT_DATE].dt.hour <= to_hour))
    df.loc[overtime_selector, OVERTIME] = 1
    df_overtime = df[[SENDER, OVERTIME]].groupby(SENDER).sum()
    return pd.DataFrame(df_overtime, columns=[OVERTIME])


def calculate_work_at_weekend(df):
    SATURDAY = 5
    SUNDAY = 7

    df[WORK_AT_WEEKEND] = 0
    weekend_selector = (df[EVENT_DATE].dt.weekday == SATURDAY) | (df[EVENT_DATE].dt.weekday == SUNDAY)
    df.loc[weekend_selector, WORK_AT_WEEKEND] = 1
    df_weekend = df[[SENDER, WORK_AT_WEEKEND]].groupby(SENDER).sum()
    return pd.DataFrame(df_weekend, columns=[WORK_AT_WEEKEND])
