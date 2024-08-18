# filter out names with unwanted words
# split into two databases -> those with websites and those without
# search for keywords for those with websites and tag -> if broken link, move to no website
# somehow deal with those without websites -> google search???
import pandas as pd
import urllib.request

# for importing flags
def getNames(list):
    val = []
    for s in list:
        name = s.split(',')
        for n in name: 
            val.append(n)
    return val

# import flags
temp = pd.read_csv('data-scrape/flags.csv', usecols=[1])["Nation"].to_list()
nation = getNames(temp)
temp = pd.read_csv('data-scrape/flags.csv', usecols=[2])["People"].to_list()
people = getNames(temp)
temp = pd.read_csv('data-scrape/flags.csv', usecols=[3])["Languages"].to_list()
language = getNames(temp)

flags = dict.fromkeys(set(nation + people + language), False)

link = "https://willingdon.org/ilm"
site_content = urllib.request.urlopen(link).read().decode("utf-8")

print(site_content)

for word in flags:
    if word in site_content:
        flags[word] = True

print(flags)