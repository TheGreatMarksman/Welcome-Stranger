# code adapted from: https://www.scrapingdog.com/blog/scrape-google-search-results/

import requests
from bs4 import BeautifulSoup
import pandas as pd

headers={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36'}
API_KEY = "AIzaSyAxkrgYIReoiF5V7kGrkfoHwoPYsT3GaUU" # need to create a *legal* google search api key and insert here
CX_KEY = "91d6a82417b9a4c87" # need to create a custom search engine and insert key here


#org_names = pd.read_csv('raw-data/canadian-registered-charities.csv', usecols=[1])['Organization name'].to_list()
org_names = ["Willingdon church", "Riverside Church", "Coquitlam Alliance Church", "Oprah", "église" , "Christ Jesus"]
Data = [ ] # Data ends up being a list of dictionaries

# initialize keywords list
keywords = ["christ", "church", "jesus", "eglise", "église", "jésus"]

for name in org_names:
    search_string = name.replace(' ', '+')
    url = "https://www.googleapis.com/customsearch/v1?key=" + API_KEY + "&cx=" + CX_KEY + "q=" + search_string + "&num=1"
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
                g=g+1
                try: title=allData[i].find('h3',{"class":"DKV0Md"}).text
                except: title=None

                try: description=allData[i].find("div",{"class":"VwiC3b"}).text
                except: description=None

                print(name)
                #print(description)

                for word in keywords:
                    if not description == None and not title == None and not name == None: 
                        if name.lower().find(word) >= 0 or description.lower().find(word) >= 0 or title.lower().find(word) >= 0:
                            l["name"] = name
                            l["link"]=link
                            l["title"]=title
                            Data.append(l)
                            break

                l={}

            else:
                continue

        else:
            continue

df = pd.DataFrame(Data)
df.to_csv('google-results.csv', index=False, encoding='utf-8')