import pandas as pd

def fraggin_table(events_df):
    #first we want to FILTER for kills
    events_filtered_by_kills = events_df.query('type == "CHAMPION_KILL"')
    events_filtered_by_kills.dropna()

    