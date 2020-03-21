#!/usr/bin/env python3
# coding: utf-8

import random
from datetime import datetime

import pandas as pd
import sqlalchemy as sa


n_institutions = 4000

institution_ids = range(n_institutions)
resource_types = ["Betten", "IPS-Betten ohne Beatmung", "IPS-Betten mit Beatmung", "Nicht-IPS-Betten mit Beatmung", "COVID-Betten", "Herz-Lungen-Geräte"]
possible_max_capacities = range(100, 525, 25)

max_capacities = [(institution_id, resource_type, random.choice(possible_max_capacities)) for institution_id in institution_ids for resource_type in resource_types]
resources = [(institution_id, resource_type, max_cap, random.choice(range(max_cap + 1)), datetime.now()) for institution_id, resource_type, max_cap in max_capacities]

column_names = ["institution_id", "resource_type", "current_capacity", "max_capacity", "timestamp"]

df_import = pd.DataFrame(resources, columns=column_names, dtype=)

with open ("connection", "r") as myfile:
    conStr = myfile.readlines()[0]

sqlCon = sa.create_engine(conStr)

df_import.to_sql(name="resources", con=sqlCon, index=False, if_exists="append")
