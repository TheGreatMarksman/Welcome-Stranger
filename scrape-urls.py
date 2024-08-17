# code adapted from: https://www.scrapingdog.com/blog/scrape-google-search-results/

import requests
from bs4 import BeautifulSoup
import pandas as pd

headers={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36'}

org_names = pd.read_csv('raw-data/canadian-registered-charities.csv', usecols=[1])['Organization name'].to_list()
#org_names = ["Willingdon church", "Coquitlam Alliance Church", "Riverside Church"]
Data = [ ] # Data ends up being a list of dictionaries

for name in org_names:
    search_string = name.replace(' ', '+')
    url = "https://www.google.com/search?q=" + search_string + "&num=1"
    #url='https://www.google.com/search?q=dragon&ie=utf-8&oe=utf-8&num=10'
    
    html = requests.get(url,headers=headers)
    #print(html.status_code)
    # if status code not 200, there's a problem

    soup = BeautifulSoup(html.text, 'html.parser')
    allData = soup.find_all("div",{"class":"g"})

    g=0
    l={} # each dictionary has keys link, title, description, position
    for i in range(0,len(allData)):
        link = allData[i].find('a').get('href')

        if(link is not None):
            if(link.find('https') != -1 and link.find('http') == 0 and link.find('aclk') == -1):
                l["name"] = name
                g=g+1
                l["link"]=link
                try: l["title"]=allData[i].find('h3',{"class":"DKV0Md"}).text
                except: l["title"]=None

                try: l["description"]=allData[i].find("div",{"class":"VwiC3b"}).text
                except: l["description"]=None

                l["position"]=g

                Data.append(l)

                l={}

            else:
                continue

        else:
            continue

df = pd.DataFrame(Data)
df.to_csv('google-results.csv', index=False, encoding='utf-8')