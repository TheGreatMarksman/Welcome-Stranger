from selenium import webdriver
import re
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import pandas as pd
import time
from bs4 import BeautifulSoup

# code adapted from: https://www.scrapehero.com/scrape-data-from-data-layer-of-google-tag-manager/

#org_names = pd.read_csv('raw-data/van-registered.csv', usecols=[1])['Organization name'].to_list()
url = "https://www.charitydata.ca/charity/acces-accessible-community-counselling-and-employment-services/136747276RR0001/"
Data = []

driver = webdriver.Chrome()
driver.get(url)
time.sleep(3)
page = driver.page_source
driver.quit
soup = BeautifulSoup(page, 'html.parser')

info = []
dt_data = soup.find_all("dt")
dd_data = soup.find_all("dd")

# Now you can process the data as needed
l = {}
'''for dt_item, dd_item in zip(dt_data, dd_data):
    name = dt_item.text.strip()
    value = dd_item.text.strip()
    l[name] = value
    print(f"Name: {name} Value: {value}")'''
for dt_item, dd_item in zip(dt_data, dd_data):
    l[dt_item.text.strip()] = dd_item.text.strip()
Data.append(l)
l = {}

'''
for url_ in elem:
    try:
        print(url_.get_attribute("href"))
        newdriver = webdriver.Chrome()
        newdriver.get(url_.get_attribute("href"))
        newdriver.close()
    except Exception as e:
        print(e)
        newdriver.close()
'''


driver.close()
df = pd.DataFrame(Data)
df.to_csv('google-results.csv', index=False, encoding='utf-8')