import requests
import pandas as pd

# get the API KEY here: https://developers.google.com/custom-search/v1/overview
API_KEY = " "
# get your Search Engine ID on your CSE control panel
SEARCH_ENGINE_ID = " "

org_names = pd.read_csv('raw-data/van-registered.csv', usecols=[1])['Organization name'].to_list()
#org_names = ["Willingdon church", "Riverside Church", "Coquitlam Alliance Church", "Oprah", "église" , "Christ Jesus"]
Data = [ ] # Data ends up being a list of dictionaries

# initialize keywords list
keywords = ["christ", "church", "jesus", "eglise", "église", "jésus"]

# the search query you want
for query in org_names:
    # constructing the URL
    # doc: https://developers.google.com/custom-search/v1/using_rest
    url = f"https://www.googleapis.com/customsearch/v1?key={API_KEY}&cx={SEARCH_ENGINE_ID}&q={query}&num=1"

    # make the API request
    data = requests.get(url).json()

    # get the result items
    search_items = data.get("items")
    l={} # each dictionary has keys link, title, description, position
    # iterate over 10 results found
    for i, search_item in enumerate(search_items, start=1):
        try:
            long_description = search_item["pagemap"]["metatags"][0]["og:description"]
        except KeyError:
            long_description = "N/A"
        # get the page title
        title = search_item.get("title")
        # page snippet
        snippet = search_item.get("snippet")
        # alternatively, you can get the HTML snippet (bolded keywords)
        # html_snippet = search_item.get("htmlSnippet")

        for word in keywords:
            if not query == None and not title == None and not snippet == None: 
                if query.lower().find(word) >= 0 or title.lower().find(word) >= 0 or snippet.lower().find(word) >= 0:
                    l["name"] = query
                    l["link"]=search_item.get("link")
                    l["title"]=title
                    l["snippet"]=snippet
                    Data.append(l)
                    print(query)
                    break

        l={}

df = pd.DataFrame(Data)
df.to_csv('google-results.csv', index=False, encoding='utf-8')