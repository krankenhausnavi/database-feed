import os
import time
import json

from bs4 import BeautifulSoup, element
import requests


API_URL = "https://dienste.kvb.de/arztsuche/app/suchergebnisse.htm?hashwert=3f48bfa494c160a935e7a18bee17&page={}&zeigeKarte=true&resultCount=19000"
LAST_PAGE = 1159


def main():
    doctors = []
    opening_times = []
    for i in range(1, 20):
        print(i)
        bs = _get_html(API_URL.format(i), None, f"by/{i}.html")
        try:
            d, o = _parse_page(bs, i*10 - 10)
            doctors.extend(d)
            opening_times.extend(o)
        except Exception as e:
            print(e)
            continue

    with open("doctors_by.json", "w") as f:
        json.dump(doctors, f)
    with open("opening_times_by.json", "w") as f:
        json.dump(opening_times, f)


def _parse_page(bs, id_start):
    doctors = []
    opening_times = []

    res_div = bs.find("div", class_="suchergebnisse_liste")
    for i, row in enumerate(res_div.find_all("div", class_="suchergebnisse_praxis_tabelle")):
        main_table = row.find("table")

        name = "{} ({})".format(main_table.find("td", class_="titel_name_zelle").text.strip(),
                                main_table.find("td", class_="fachgebiet_zelle").text.strip())

        address_table = main_table.find("table", class_="adresse_tabelle")
        address_parts = address_table.find_all("tr")
        street = address_parts[-2].text.strip()
        plz, city = tuple(address_parts[-1].text.strip().split("\xa0", 1))

        contact_table = main_table.find("table", class_="tel_tabelle")
        tel = None
        mail = None
        website = None
        for row in contact_table.find_all("tr"):
            text = row.text.strip()
            if text.startswith("Tel"):
                tel = row.find_all("td")[1].text.strip()
            if text.startswith("E-Mail"):
                mail = row.find_all("td")[1].text.strip()
            if text.startswith("Web"):
                website = row.find_all("td")[1].text.strip()

        comment = None

        times_table = main_table.find("table", class_="sprechzeiten_tabelle")
        for row in times_table.find_all("tr"):
            day = row.find("td", class_="wochentag")
            time = row.find("td", class_="uhrzeiten")
            if day is not None:
                day_name = {
                    "Mo:": "Montag",
                    "Di:": "Dienstag",
                    "Mi:": "Mittwoch",
                    "Do:": "Donnerstag",
                    "Fr:": "Freitag",
                    "Sa:": "Samstag",
                    "So:": "Sonntag"
                }[day.text.strip()]
                times_parts = time.text.strip().split(" ")
                for times_part in times_parts:
                    opening_times.append({
                        "institution_id": id_start + i,
                        "day": day_name,
                        "start": times_part.split("-")[0],
                        "end": times_part.split("-")[1]
                    })
            else:
                if row.text.strip() == "und nach Vereinbarung":
                    comment = "Sprechzeiten auch nach Vereinbarung"
                break  # Skipping other types of opening times now

        doctors.append({
            "id": id_start + i,
            "name": name,
            "type": "doctor",
            "street": street,
            "city": city,
            "postcode": plz,
            "phone": tel,
            "email": mail,
            "website": website,
            "comment": comment,
        })

    return doctors, opening_times



def _get_html(url, params, cache_fname):
    cache_path = os.path.join(os.path.dirname(__file__), "cache", cache_fname)
    if os.path.exists(cache_path):
        with open(cache_path) as f:
            return BeautifulSoup(f.read(), "lxml")
    else:
        r = requests.get(url, params)
        time.sleep(0.5)  # Not the best place to put this
        with open(cache_path, "w") as f:
            f.write(r.text)
        return BeautifulSoup(r.text, "lxml")


if __name__ == "__main__":
    main()
