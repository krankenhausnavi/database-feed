#!/usr/bin/env python3
# coding: utf-8
import random
from datetime import datetime
import pandas as pd
import sqlalchemy as sa

n_institutions = 4000

institution_ids = range(n_institutions)
service_types = {"Hausbesuch", "Notfalltermin", "Telefonauskunft"}

column_names = ["institution_id", "service_type", "waiting_time", "timestamp"]

waiting_times = [(i_id,
                  s_type,
                  random.randint(0,60)*5,
                  int(datetime.now().timestamp()))
                 for s_type in service_types
                 for i_id in institution_ids
                 if random.random() < 0.5]

df_import = pd.DataFrame(waiting_times, columns=column_names)

with open ("connection", "r") as myfile:
    conStr = myfile.readlines()[0]

sqlCon = sa.create_engine(conStr)

df_import.to_sql(name="waiting_times", con=sqlCon, index=False, if_exists="append")

