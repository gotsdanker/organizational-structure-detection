from manufacturing_company.src.common.const import *


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


