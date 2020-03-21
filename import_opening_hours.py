#!/usr/bin/env python3
# coding: utf-8


import random

import pandas as pd


n_institutions = 2000

institution_ids = range(n_institutions)
days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]
times = [("7:00", "12:00"), ("13:00", "18:00")]

possible_opening_hours = [(day, start, end) for day in days for start, end in times]

column_names = ["institution_id", "day", "start_time", "end_time"]

opening_hours = [(institution_id, day, start, end) for institution_id in institution_ids for day, start, end in random.sample(possible_opening_hours, 6)]
df_import = pd.DataFrame(opening_hours, columns=column_names)

df_import.to_csv("opening_hours.csv", index=False)