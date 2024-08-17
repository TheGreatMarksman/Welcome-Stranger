import pandas as pd
import requests
import re

orgs = pd.read_csv("first-pass.csv", usecols=[0,1], dtype={"name":"str", "link":"str"}) # name, link
#orgs = orgs.head()
org_links = orgs["link"].to_list()

headers={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36'}
contact_pages = []
expression = re.compile(r"(.+\.(ca|com|org))")

for url in org_links:
    success = False
    tries = [url+"contact/",url+"contact-us",url+"connect",url+"contactus",
             url+"/contact/",url+"/contact-us", url+"/connect",url+"/contactus"]
    match = expression.search(url) # does not work if facebook page, for ex
    if match: tries.extend([match.group(1)+"/contact/",match.group(1)+"/contact-us",match.group(1)+"/connect",match.group(1)+"/contactus"])
    for try_url in tries:
        if success==True: break
        try:
            html = requests.get(try_url, headers=headers)
            if html.status_code==200:
                page = {}
                page["link"] = url
                page["contact page"] = try_url
                contact_pages.append(page)
                success = True
        except:
            pass


contact_pages_df = pd.DataFrame(contact_pages, dtype="str") # link, contact page
contact_pages_df.drop_duplicates(inplace=True)

new_orgs = orgs.merge(contact_pages_df, on="link", how="left")
new_orgs.to_csv("contact-pages.csv")