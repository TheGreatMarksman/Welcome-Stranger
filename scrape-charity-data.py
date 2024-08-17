from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import pandas as pd
from bs4 import BeautifulSoup

# code adapted from: https://www.scrapehero.com/scrape-data-from-data-layer-of-google-tag-manager/

#org_names = pd.read_csv('raw-data/van-registered.csv', usecols=[1])['Organization name'].to_list()
url = "https://www.charitydata.ca/charity/acces-accessible-community-counselling-and-employment-services/136747276RR0001/"

driver = webdriver.Chrome()
driver.get(url)
try:
    elem = driver.find_elements(By.XPATH, "/html/body/main/section[1]/div/div[1]/dl/dd[5]/a")
    print(f"elem: {elem}") # gets an empty list
except Exception as e:
    print(e)
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
