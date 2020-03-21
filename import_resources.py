#!/usr/bin/env python3
# coding: utf-8

import random

import pandas as pd
import sqlalchemy as sa


n_institutions = 2000

institution_ids = range(n_institutions)
resource_types = ["Betten", "Itensivbetten", "Beatmungsgeräte"]
max_capacities = range(100, 525, 25)

column_names = ["institution_id", "resource_type", "max_capacity"]

resources = [(institution_id, resource_type, random.choice(max_capacities)) for institution_id in institution_ids for resource_type in resource_types]
df_import = pd.DataFrame(resources, columns=column_names)

conStr = ""

with open ("connection", "r") as myfile:
    conStr = myfile.readlines()[0]

sqlCon = sa.create_engine(conStr)

df_import.to_sql(name="institutions", con=sqlCon, index=False, if_exists="append")
