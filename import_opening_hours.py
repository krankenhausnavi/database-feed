#!/usr/bin/env python3
# coding: utf-8


import random

import pandas as pd
import sqlalchemy as sa


n_institutions = 4000

institution_ids = range(n_institutions)
days = ["Montag", "Dienstag", "Mittwoch", "Donnerstag", "Freitag", "Samstag"]
times = [("7:00", "12:00"), ("13:00", "18:00")]

possible_opening_hours = [(day, start, end) for day in days for start, end in times]

column_names = ["institution_id", "day", "start_time", "end_time"]

opening_hours = [(institution_id, day, start, end) for institution_id in institution_ids for day, start, end in random.sample(possible_opening_hours, 6)]
df_import = pd.DataFrame(opening_hours, columns=column_names)

with open ("connection", "r") as myfile:
    conStr = myfile.readlines()[0]

sqlCon = sa.create_engine(conStr)

df_import.to_sql(name="opening_hours", con=sqlCon, index=False, if_exists="append")
