import pandas as pd

filter_words = ["jehova", "jehova's witness", "mormon", "latter day", "latter day saints", "joseph smith", "lds", "god the mother", 
          "jéhova", "mormone", "mormonisme", "saints des derniers jours", "derniers jours", "dieu la mère"]

data = pd.read_csv("data-scrape/data/raw-data/charity-data-links-descriptions.csv")

for word in filter_words:
    filter = ~data["name"].str.contains(word, case=False)
    data = data.loc[filter]

data.to_csv("data-scrape/data/transformed-data/charity-data-links-descriptions-filtered.csv")

## Lucy's area

