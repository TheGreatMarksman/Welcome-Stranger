import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By

# code adapted from: https://www.scrapehero.com/scrape-data-from-data-layer-of-google-tag-manager/

MAX_NUM_SEARCH_RESULTS = "26000"

headers={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36'}
list_url = "https://www.charitydata.ca/search?fpeYear=2022&pageSize="+MAX_NUM_SEARCH_RESULTS+"&sortBy=relevance&sortDirection=asc&offset=0&descriptionCode=c&categoryCode=30"
Data = []

driver = webdriver.Chrome()
driver.implicitly_wait(100)
driver.get(list_url)

try:
    elem = driver.find_elements(By.XPATH, "/html/body/main/div/div[2]/div/article/a/h4")
    for url in elem:
        l = {}
        l["name"] = url.text
        also_elem = url.find_elements(By.XPATH, "./..")
        for also_url in also_elem:
            l["charity data link"] = also_url.get_attribute("href")
        Data.append(l)
except Exception as e:
    print(e)

df = pd.DataFrame(Data)
df.to_csv('charity-data-links.csv', index=False, encoding='utf-8')