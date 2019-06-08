from manufacturing_company.src.common.const import *
import numpy as np


def assign_management_levels_cc(levels, df_employees, df_positions):
    print('ok')
    if levels == 2:
        df_employees[POSITION] = 2
        management_level = df_positions[df_positions[POSITION].isin(np.arange(1, levels))].index
        df_employees.loc[df_employees.index.isin(management_level), POSITION] = 1
    elif levels == 3:
        df_employees[POSITION] = 3

        first_management_level = df_positions[df_positions[POSITION] == 1].index
        second_management_level = df_positions[df_positions[POSITION] == 2].index

        df_employees.loc[df_employees.index.isin(first_management_level), POSITION] = 1
        df_employees.loc[df_employees.index.isin(second_management_level), POSITION] = 2
    else:
        raise Exception("Unsupported number of levels")

    return df_employees
