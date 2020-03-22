#!/usr/bin/env python3
# coding: utf-8

import json

import pandas as pd

import sqlalchemy as sa

hospitals_json = 'hospitals.json'

with open(hospitals_json, 'r') as f:
    hospitals = json.load(f)

column_names = ["name", "type", "street", "city", "postcode", "phone", "website", "email", "lat", "lon", "comment"]

df_import = pd.DataFrame(hospitals, columns=column_names)

with open ("connection", "r") as myfile:
    conStr = myfile.readlines()[0]

sqlCon = sa.create_engine(conStr)

df_import.to_sql(name="institutions", con=sqlCon, index=False, if_exists="append")
