#!/usr/bin/env python
# coding: utf-8

# In[2]:


import json
import urllib.request

import pandas as pd


# In[9]:


import_url_doctors = "https://services7.arcgis.com/mOBPykOjAyBO2ZKk/arcgis/rest/services/Arzt_doctors/FeatureServer/0/query?where=1%3D1&outFields=*&outSR=4326&f=json"

with urllib.request.urlopen(import_url_doctors) as response:
    data = json.loads(response.read().decode())


# In[16]:


processed_data = [{**item["attributes"], **item["geometry"]} for item in data["features"]]


# In[19]:


df_doctors = pd.DataFrame(processed_data)


# In[80]:


df_doctors_clean = df_doctors[~df_doctors.name.isna()]


# In[101]:


df_doctors_clean = df_doctors_clean[
    ~df_doctors_clean.address_city.isna()
    & ~df_doctors_clean.address_street.isna()
    & ~df_doctors_clean.address_housenumber.isna()
    & ~df_doctors_clean.address_postcode.isna()]

column_names = ["name", "type", "street", "city", "postcode", "phone", "website", "email", "lat", "long", "comment"]

df_import = pd.DataFrame(columns=column_names)

df_import.name = df_doctors_clean.name
df_import.type = "doctor"
df_import.street = df_doctors["address_street"] + " " + df_doctors["address_housenumber"]
df_import.city = df_doctors["address_city"]
df_import.postcode = df_doctors["address_postcode"]
df_import.phone = df_doctors["contact_phone"]
df_import.email = df_doctors["contact_email"]
df_import.website = df_doctors["contact_website"]
df_import.lat = df_doctors["y"]
df_import.long = df_doctors["x"]
df_import.comment = "TODO"


# In[106]:


df_import.to_sql("doctors.csv", index=False)

