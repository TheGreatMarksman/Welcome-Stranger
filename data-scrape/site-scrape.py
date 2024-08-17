# filter out names with unwanted words
# split into two databases -> those with websites and those without
# search for keywords for those with websites and tag -> if broken link, move to no website
# somehow deal with those without websites -> google search???
import urllib.request
site_content = urllib.request.urlopen(link).read().decode("utf-8")

keywords = ['word', 'word1', 'word2']
for word in keywords:
    if word in site_content:
        print(f"{word} found")
    else:
        print(f"{word} not found")


filter = ["jehova", "jehova's witness", "mormon", "latter day", "latter day saints", "joseph smith", "lds", "god the mother", 
          "jéhova", "mormone", "mormonisme", "saints des derniers jours", "derniers jours", "dieu la mère"]

nolink = []