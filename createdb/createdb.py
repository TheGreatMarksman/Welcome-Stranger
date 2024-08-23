import sqlite3
import pandas as pd
import json

db = sqlite3.connect('../organizations.db')

language_text = """
Unkown
Persian, Farsi
Dari, Pashto, Uzbek, Turkmen, Balochi, Pashayi
Somali, Maay, Baraawe, Chiminii, Arabic
Arabic, Kurdish, Armenian, Circassian
Turkish, Kurdish, Zazaki, Arabic
Punjabi, Hindi
Bangla
Bosnian, Serbian, Croatian
Uyghur
Tibetan
Sinhala, Helabasa, Tamil
Palestinian, Arabic, Palestinina Arabic
Urdu
Arabic, Spanish, French
Lebanese, Arabic, Lebanese Arabic
Hebrew
Hindi
Gujarati
Egyptian, Arabic, Egyptian Arabic
Khmer
Arabic, Tamazight
Tunisian Arabic, French, Berber, Arabic
Korean
Nihongo
Chinese, Cantonese
"""

ORGANIZATION_DATA_FILE = "../data-scrape/sample-org-data.csv"
START_FILE = "../data-scrape/data/raw-data/canadian-registered-charities.csv"
CONTACT_FILE = "../data-scrape/data/contact-info-results-1000.csv"
NATION_FILE = "../nations.json"

languages = [l for l in ', '.join(language_text.splitlines()).split(', ') if l]

with open(NATION_FILE) as f:
    nationList = json.load(f)
    
nations = ['unkown'] + list(set(nation for org in nationList for nation in nationList[org]))

def load_csv_to_memory(file_path):
    """
    Load a CSV file into memory as a pandas DataFrame.
    """
    return pd.read_csv(file_path)

def find_row_in_data(data, column_name, value):
    """
    Find rows in a DataFrame where the specified column matches the given value.
    """
    result = data[data[column_name] == value]
    return result.iloc[0] if not result.empty else None

with open('schema.sql') as f:
    db.executescript(f.read())

for language in languages:
    db.execute("INSERT INTO languages (name) VALUES (?)", [language])

for nation in nations:
    db.execute("INSERT INTO nations (name) VALUES (?)", [nation])

base_data = load_csv_to_memory(START_FILE)
org_data = load_csv_to_memory(ORGANIZATION_DATA_FILE)
contact_data = load_csv_to_memory(CONTACT_FILE)

cursor = db.cursor()

cities = set()

for _, row in base_data.iterrows():
    city = row['City']
    province = row["Province, territory, outside of Canada"]
    cities.add((city, province))

city_map = {}
for city, province in cities:
    if isinstance(province, float) or province == "nan": continue
    cursor.execute("""
    INSERT INTO cities (name, province)
    VALUES (?, ?)
    """, [city, province])
    city_map[f'{city}/{province}'] = cursor.lastrowid

addedCount = 0
for _, org_row in org_data.iterrows():
    id = org_row['id']
    
    base_row = find_row_in_data(base_data, 'BN/Registration Number', id)
    contact_row = find_row_in_data(contact_data, 'Business Registration Number:', id)
    
    if base_row is None: 
        print(f'No match in base data. Skipping {id}.')
        continue
    if contact_row is None: 
        print(f'No match in contact data. Skipping {id}.')
        continue
    
    if id not in nationList: 
        supportedNations = []
    else: 
        supportedNations = nationList[id]

    name = org_row['name']
    address = base_row['Address']
    email = contact_row['email'] if contact_row is not None else "N/A"
    phone = contact_row['phone'] if contact_row is not None else "N/A"
    description = org_row['description']
    website = org_row['website']

    city = base_row['City']
    province = base_row["Province, territory, outside of Canada"]

    if f'{city}/{province}' not in city_map: continue
    cityid = city_map.get(f'{city}/{province}', 0)

    cursor.execute("""
    INSERT INTO organizations (name, website, phone, email, description)
    VALUES (?, ?, ?, ?, ?)
    """, [name, website, phone, email, description])

    org_id = cursor.lastrowid

    cursor.execute("""
    INSERT INTO locations (organization_id, city_id, address, has_service)
    VALUES (?, ?, ?, ?)
    """, [org_id, cityid, address, 0])
    
    location_id = cursor.lastrowid
    
    for nation in supportedNations:
        nationId = nations.index(nation) + 1
        cursor.execute("""
        INSERT INTO location_languages (location_id, language_id, nation_id)
        VALUES (?, ?, ?)
        """, [location_id, 1, nationId])
    addedCount += 1
    
print(f"Added {addedCount} organizations")

# Commit the transaction and close the database
db.commit()
db.close()