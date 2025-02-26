import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By

# code adapted from: https://www.scrapehero.com/scrape-data-from-data-layer-of-google-tag-manager/

MAX_NUM_SEARCH_RESULTS = "26000" # to get all results on the same page

headers={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36'}
list_url = "https://www.charitydata.ca/search?fpeYear=2022&pageSize="+MAX_NUM_SEARCH_RESULTS+"&sortBy=relevance&sortDirection=asc&offset=0&descriptionCode=c&categoryCode=30"
Data = []
filter_words = ["jehova", "jehova's witness", "mormon", "latter day", "latter day saints", "joseph smith", "lds", "god the mother", 
          "jéhova", "mormone", "mormonisme", "saints des derniers jours", "derniers jours", "dieu la mère"]

# request the Charity Data search page
driver = webdriver.Chrome()
driver.implicitly_wait(100)
driver.get(list_url)

try:
    # get the name, Charity Data link, and description of each charity
    elements = driver.find_elements(By.XPATH, "/html/body/main/div/div[2]/div/article/a")
    for elem in elements:
        l = {}
        all_text = elem.text
        all_text = all_text.splitlines()
        skip = False
        for word in filter_words:
            for section in all_text:
                if word in section:
                    skip = True
                    break
        if skip==False:
            l["name"] = all_text[0]
            l["charity data link"] = elem.get_attribute("href")
            try: l["description"] = all_text[1]
            except: pass
            Data.append(l)
except Exception as e:
    print(e)

driver.close()

df = pd.DataFrame(Data)
df.to_csv('data-scrape/data/raw-data/charity-data-links-descriptions.csv', index=False, encoding='utf-8')