#!/usr/bin/env python3
# coding: utf-8

import re
from tqdm import tqdm

import json
import urllib.request
from bs4 import BeautifulSoup

import pandas as pd

url = "https://www.weisse-liste.de/ajax/ajax.html?searchType=HOSPITAL_NAME&searchDistance=ALL&include=hospitalResult&offset=0&limit=3000"

with urllib.request.urlopen(url) as response:
    soup = BeautifulSoup(response.read())

hospital_soup = soup.find_all("li", "resultItem")

hospitals = []

for item in tqdm_notebook(hospital_soup): 
    detail_url = f"https://www.weisse-liste.de/de/krankenhaus/krankenhaussuche/ergebnisliste/profil/;jsessionid=D2C14A55878C11F69B2E914CC584CC70?id={item['id']}&searchType=HOSPITAL_NAME&type=hospital"
        
    with urllib.request.urlopen(detail_url) as response:
        detail_soup = BeautifulSoup(response.read()) #read in
                
    name = item["data-title"]
    street = item.find(itemprop="streetAddress").contents[0]
    city = item.find(itemprop="addressLocality").contents[0]
    postcode = item.find(itemprop="postalCode").contents[0]
    phone = re.search(r'(?<=Tel\.\:\s)(.*)(?=\r\n)', str(detail_soup.find_all("div", "compareBlock")[1].td)).group(1)
    email = detail_soup.find_all("div", "compareBlock")[1].a['href'][7:]
    if detail_soup.find("a", "externLink", itemprop="url"):
        website = detail_soup.find("a", "externLink", itemprop="url").contents[0]
    else:
        website = None
    comment = None
    lat = item["data-lat"]
    lon = item["data-lng"]

    hospitals.append({
        "name": name,
        "type": "hospital",
        "street": street,
        "city": city,
        "postcode": postcode,
        "phone": phone,
        "email": email,
        "website": website,
        "comment": None,
        "lat": lat,
        "lon": lon,
    })

hospitals_json = 'hospitals_from_weisse_liste.json'

with open(hospitals_json, 'w') as f:
    json.save(hospitals, f)
