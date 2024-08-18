from selenium import webdriver
import pandas as pd
import time
from bs4 import BeautifulSoup

# code adapted from: https://www.scrapehero.com/scrape-data-from-data-layer-of-google-tag-manager/

links_list = pd.read_csv('data-scrape/data/test-data-1000.csv', usecols=[1])["charity data link"].to_list()
Data = []
driver = webdriver.Chrome()

for link in links_list:
    driver.get(link)
    time.sleep(1) # to ensure all data has been loaded
    page = driver.page_source
    soup = BeautifulSoup(page, 'html.parser')

    info = []
    dt_data = soup.find_all("dt")
    dd_data = soup.find_all("dd")

    # Get table data as pairs and add to dictionary
    l = {}
    for dt_item, dd_item in zip(dt_data, dd_data):
        l[dt_item.text.strip()] = dd_item.text.strip()
    Data.append(l)
    l = {}

driver.close()
df = pd.DataFrame(Data)
df.to_csv('data-scrape/data/test-results-1000.csv', index=False, encoding='utf-8')