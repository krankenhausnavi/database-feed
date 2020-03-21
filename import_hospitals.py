#!/usr/bin/env python3
# coding: utf-8

import json
import urllib.request

import pandas as pd

import sqlalchemy as sa

import_url_hospitals = "https://services7.arcgis.com/mOBPykOjAyBO2ZKk/arcgis/rest/services/Krankenhaus_hospital/FeatureServer/0/query?where=1%3D1&outFields=*&outSR=4326&f=json"

with urllib.request.urlopen(import_url_hospitals) as response:
    data = json.loads(response.read().decode('latin-1', 'ignore'))

processed_data = [{**item["attributes"], **item["geometry"]} for item in data["features"]]

df_hospitals = pd.DataFrame(processed_data)
df_hospitals_clean = df_hospitals[
    ~df_hospitals.name.isna()
    & ~df_hospitals.address_city.isna()
    & ~df_hospitals.address_street.isna()
    & ~df_hospitals.address_housenumber.isna()
    & ~df_hospitals.address_postcode.isna()]

column_names = ["name", "type", "street", "city", "postcode", "phone", "website", "email", "lat", "lon", "comment"]

df_import = pd.DataFrame(columns=column_names)

df_import.name = df_hospitals_clean.name
df_import.type = "hospital"
df_import.street = df_hospitals_clean["address_street"] + " " + df_hospitals_clean["address_housenumber"]
df_import.city = df_hospitals_clean.address_city
df_import.postcode = df_hospitals_clean.address_postcode
df_import.phone = df_hospitals_clean.contact_phone
df_import.email = df_hospitals_clean.contact_email
df_import.website = df_hospitals_clean.contact_website
df_import.lat = df_hospitals_clean.y
df_import.lon = df_hospitals_clean.x
df_import.comment = "TODO"

conStr = ""

with open ("connection", "r") as myfile:
    conStr = myfile.readlines()[0]

sqlCon = sa.create_engine(conStr)

df_import.to_sql(name="institutions", con=sqlCon, index=False, if_exists="append", )
