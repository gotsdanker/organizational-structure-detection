from manufacturing_company.src.common.const import *
import numpy as np
import pandas as pd
from sklearn.metrics import jaccard_score


def neighbors_per_month_sender(df, G):
    df_tmp = df.groupby([SENDER, df[EVENT_DATE].dt.month])[RECIPIENT].unique()
    df_tmp = pd.DataFrame(df_tmp)
    df_tmp.index.names = [ID, EVENT_DATE]
    return fill_missing_neighbors(df_tmp, G)


def neighbors_per_month_recipient(df, G):
    df_tmp = df.groupby([RECIPIENT, df[EVENT_DATE].dt.month])[SENDER].unique()
    df_tmp = pd.DataFrame(df_tmp)
    df_tmp.index.names = [ID, EVENT_DATE]
    return fill_missing_neighbors(df_tmp, G)


def neighbors_per_month_sender_and_recipient(df_sender, df_recipient):
    df_sender_recipient = pd.merge(df_sender, df_recipient, how='outer', on=[ID, EVENT_DATE]).sort_index()
    df_sender_recipient = df_sender_recipient.apply(merge_contacted_ids, axis=1)
    df_sender_recipient = pd.DataFrame(df_sender_recipient)
    df_sender_recipient.index.names = [ID, EVENT_DATE]
    return df_sender_recipient


def merge_contacted_ids(row):
    if row[0] is np.NaN:
        return row[1]
    if row[1] is np.NaN:
        return row[0]
    msg_x = np.array(row[0])
    msg_y = np.array(row[1])
    return msg_x | msg_y


def fill_missing_neighbors(df, G):
    all_employees = pd.Series(G.nodes)
    df.iloc[:, 0] = df.apply(lambda row: all_employees.isin(row[0]).tolist(), axis=1)
    return df


def calculate_neighborhood_variability(df, G):
    df_sender = neighbors_per_month_sender(df, G)
    df_recipient = neighbors_per_month_recipient(df, G)
    df_sender_recipient = neighbors_per_month_sender_and_recipient(df_sender, df_recipient)

    neighborhood_variability_sender = calculate_jaccard(df_sender)
    neighborhood_variability_recipient = calculate_jaccard(df_recipient)
    neighborhood_variability_sender_recipient = calculate_jaccard(df_sender_recipient)

    return neighborhood_variability_sender, neighborhood_variability_recipient, neighborhood_variability_sender_recipient


def calculate_jaccard(df):
    employee_ids = df.index.get_level_values(0).unique()

    neighborhood_variability = dict()

    for id in employee_ids:
        row = df.loc[(id, slice(None))]
        neighborhood_variability[id] = jaccard(row, id)

    return neighborhood_variability


def jaccard(rows, employee_id):
    if len(rows) < 2:
        return 0

    jaccard = []
    months = rows.index.get_level_values(0).unique()
    for month_nr in range(len(months)):
        if month_nr == len(months) - 1:
            break
        current_set = rows.loc[months[month_nr]].tolist()[0]
        next_set = rows.loc[months[month_nr+1]].tolist()[0]
        jaccard.append(jaccard_score(current_set, next_set))

    return np.mean(jaccard)


