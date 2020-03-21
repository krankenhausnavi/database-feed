#!/usr/bin/env python3
# coding: utf-8

import urllib
import dateutil.parser
import json

from fuzzywuzzy import process
import pandas as pd
import sqlalchemy as sa


def unpack_group(hospital_group):
    if not hospital_group["children"]:
        return [hospital_group]    
    else:
        hospitals = []
        for child in hospital_group["children"]:
            hospitals += unpack_group(child)
        return hospitals

# TODO: We need the real name-ID pairs from the database
institutions = {
    "Krankenhaus 1": 40,
    "Krankenhaus 2": 50,
}

def resolve_institution_id(hospital):
    insitution_name, _ = process.extractOne(hospital["name"], institutions.keys())
    return institutions[insitution_name]

res_mapping = {
    "Betten": "Betten Gesamtklinik",
    "Intensiv o. Beatmung": "IPS-Betten ohne Beatmung",
    "Intensiv m. Beatmung": "IPS-Betten mit Beatmung",
    "BeatmungsplÃ¤tze": "Nicht-IPS-Betten mit Beatmung",
    "Betten f. COVID Pat.": "COVID-Betten",
    "ECMO": "Herz-Lungen-Geräte"
}

def resolve_resource_type(resource):
    return res_mapping.get(resource["name"], None)

def parse_datetime(timestamp):
    return dateutil.parser.parse(timestamp)


import_url_resources = "https://apps.rescuetrack.com/rrb/api/v1/getData"
    
with urllib.request.urlopen(import_url_resources) as response:
    data = json.loads(response.read().decode('latin-1', 'ignore'))

hospitals = []

for child in data["folders"]:
    hospitals += unpack_group(child)

resources = []

for hospital in hospitals:
    institution_id = resolve_institution_id(hospital)
    
    for resource in hospital["resources"]:
        resource_type = resolve_resource_type(resource)
        max_cap = resource["capacity"]["total"]
        cur_cap = max_cap - resource["capacity"]["free"]
        timestamp = parse_datetime(resource["lastChanged"])
        
        if resource_type is not None:
            resources.append((institution_id, resource_type, max_cap, cur_cap, timestamp))


column_names = ["institution_id", "resource_type", "current_capacity", "max_capacity", "timestamp"]

df_import = pd.DataFrame(resources, columns=column_names)

with open ("connection", "r") as myfile:
    conStr = myfile.readlines()[0]

sqlCon = sa.create_engine(conStr)

df_import.to_sql(name="resources", con=sqlCon, index=False, if_exists="append")
