import pandas as pd


def dispatch_date_setup(start_time, end_time):
    start_time = start_time[:10]
    date_padding = ' 00:00:00'
    start_time = start_time + date_padding
    end_time = end_time[:10]
    date_padding = ' 23:55:00'
    end_time = end_time + date_padding
    return start_time, end_time


def fcas4s_finalise(data, start_time, date_col, group_cols):
    for column in data.select_dtypes(['object']).columns:
        data[column] = data[column].map(lambda x: x.strip())
    return data


def most_recent_records_before_start_time(data, start_time, date_col, group_cols):
    records_from_after_start = data[data[date_col] > start_time].copy()
    records_from_before_start = data[data[date_col] <= start_time].copy()
    records_from_before_start = records_from_before_start.sort_values(date_col)
    most_recent_from_before_start = records_from_before_start.groupby(group_cols, as_index=False).last()
    group_cols = group_cols + [date_col]
    most_recent_from_before_start = pd.merge(most_recent_from_before_start.loc[:,group_cols], records_from_before_start,
                                             'inner', group_cols)
    mod_table = pd.concat([records_from_after_start, most_recent_from_before_start])
    return mod_table
