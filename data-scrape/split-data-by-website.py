import requests
import pandas as pd

data = pd.read_csv("data-scrape/data/test-results-1000.csv", dtype="str")
# schema: Designation description:,Charity type:,Category:,Business Registration Number:,Website:,Mailing Address:

headers={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36'}

def check_link(url):
    # if the website link is "n/a" or does not work, return False
    if url=="n/a": return False
    try:
        html = requests.get("https://"+url, headers=headers)
        if html.status_code==200: return True
    except:
        pass
    try:
        html = requests.get("http://"+url, headers=headers)
        if html.status_code==200: return True
    except:
        pass
    try:
        html = requests.get(url, headers=headers)
        if html.status_code==200: return True
    except:
        return False

# split data into charities with working sites and charities without working sites
has_website = data["Website:"].apply(check_link)
data_with_websites = data[has_website]
data_without_websites = data[~has_website]

data_with_websites.to_csv("data-scrape/data/test-results-1000-with-website.csv")
data_without_websites.to_csv("data-scrape/data/test-results-1000-without-website.csv")