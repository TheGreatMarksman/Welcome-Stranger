import pandas as pd
import re

NUM_ORGS = 50 # number of organizations to use

data = pd.DataFrame() # ideal schema: id, name, website, phone, email, description

# GET ID AND NAME
name_cdlink_description = pd.read_csv("data-scrape/data/test-data-1000.csv") # schema: name, charity data link, description
name_cdlink_description = name_cdlink_description.head(NUM_ORGS)

length = name_cdlink_description.shape[0]

# extract id (charity registration #) from link
expression = re.compile(r'\d{9}RR\d{4}')
# structure of id found here:
# https://www.canada.ca/en/revenue-agency/services/charities-giving/charities/operating-a-registered-charity/registration-number.html
def get_id(link):
    try:
        return expression.search(link).group(0)
    except Exception as e:
        print("e")
        print(link)
        return None

name_cdlink_description["id"] = name_cdlink_description["charity data link"].apply(get_id)

data["id"] = name_cdlink_description["id"]
assert data.shape[0]==length
data["name"] = name_cdlink_description["name"]
assert data.shape[0]==length

id_description = name_cdlink_description[["id", "description"]]
del name_cdlink_description

# GET WEBSITE
id_website = pd.read_csv("data-scrape/data/test-results-1000.csv", usecols=[3,4])
id_website = id_website.head(NUM_ORGS)
id_website.rename(columns={"Business Registration Number:":"id","Website:":"website"}, inplace=True)

data = data.merge(id_website, how="outer", on=["id"])
assert data.shape[0]==length

del id_website

# GET PHONE AND EMAIL
# TODO: get phone and email
data["phone"] = "phone number"
data["email"] = "email"

# GET DESCRIPTION
data = data.merge(id_description, how="outer", on=["id"])
assert data.shape[0]==length

# save as csv
data.to_csv("sample-org-data.csv")