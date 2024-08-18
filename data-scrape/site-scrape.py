# filter out names with unwanted words
# split into two databases -> those with websites and those without
# search for keywords for those with websites and tag -> if broken link, move to no website
# somehow deal with those without websites -> google search???
import pandas as pd
import string

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

flags = list(set(nation + people + language))
print(flags)


import urllib.request
site_content = urllib.request.urlopen(link).read().decode("utf-8")

keywords = ['word', 'word1', 'word2']
for word in keywords:
    if word in site_content:
        print(f"{word} found")
    else:
        print(f"{word} not found")

nolink = []