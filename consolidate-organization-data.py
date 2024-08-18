import pandas as pd

data = pd.DataFrame() # ideal schema: id, name, website, phone, email, description

name = pd.read_csv("data-scrape/data/raw-data/charity-data-links-description", usecols=[0])
