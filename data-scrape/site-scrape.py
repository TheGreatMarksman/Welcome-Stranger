import pandas as pd
import urllib.request
import asyncio, aiohttp, re, gzip
import re
import validators
import json
import csv

# sitemap page locating adapted (as in directly taken) from https://stackoverflow.com/questions/56663789/how-to-get-all-pages-from-the-whole-website-using-python
async def processMapsRecursively(queue, session, mainDomain, foundPageAddresses):
    #take map address from queue and check if it responds
    map = await queue.get()
    if not map.startswith('http'):
        map = mainDomain + map
    async with session.get(map) as resp:
        if resp.status != 200:
            print(f'"{map}" returned code "{resp.status}", ignoring')
            queue.task_done()
            return None
        
        #decompress map if necessary
        if map.endswith('.gz') or map.endswith('.tgz'):
            gzFile = gzip.decompress(await resp.read())
            content = gzFile.decode()
        else:
            content = await resp.text()
    
    #if map is a map index - recurse
    if '<sitemapindex' in content:
        otherMaps = re.findall(r'<sitemap.+?<loc>\s*(.+?)\s*</loc>.+?</sitemap>', content, re.DOTALL)
        mapQueue = asyncio.Queue()
        for newMap in otherMaps:
            mapQueue.put_nowait(newMap)
        tasks = []
        for _ in range(mapQueue.qsize()):
            task = asyncio.create_task(processMapsRecursively(mapQueue, session, mainDomain, foundPageAddresses))
            tasks.append(task)
        await mapQueue.join()
        for task in tasks:
            task.cancel()
        await asyncio.gather(*tasks, return_exceptions=True)
        queue.task_done()
    
    #if map is an actual map - parse
    else:
        newPages = re.findall(r'<url.+?<loc>\s*(.+?)\s*</loc>.+?</url>', content, re.DOTALL)
        foundPageAddresses.extend(newPages)
        queue.task_done()

async def collectPagesFromMaps(sitePage):
    #locate and parse robots.txt
    mainDomain = re.match(r'https?\://[a-zA-Z0-9\-\.]+', sitePage).group(0)
    session = aiohttp.ClientSession()
    async with session.get(f'{mainDomain}/robots.txt') as resp:
        robots = await resp.text()
    mainDomain = re.match(r'https?\://[a-zA-Z0-9\-\.]+', str(resp.url)).group(0)
    siteMaps = re.findall(r'Sitemap\:\s*(.+?\.xml)', robots)
    if len(siteMaps) == 0:
        async with session.get(f'{mainDomain}/robots.txt') as resp:
            robots = await resp.text()
        siteMaps = re.findall(r'Sitemap\:\s*(.+?\.xml)', robots)
    if len(siteMaps) == 0:
        print('No maps found!')
        await session.close()
        return None
    
    #put map addresses in queue
    siteMaps = [mapFile if mapFile.startswith('http') else mainDomain + mapFile for mapFile in siteMaps]
    mapQueue = asyncio.Queue()
    for map in siteMaps:
        mapQueue.put_nowait(map)
    foundPageAddresses = []
    tasks = []
    for _ in range(mapQueue.qsize()):
        task = asyncio.create_task(processMapsRecursively(mapQueue, session, mainDomain, foundPageAddresses))
        tasks.append(task)
    
    #process all maps
    await mapQueue.join()
    for task in tasks:
        task.cancel()
    await asyncio.gather(*tasks, return_exceptions=True)
    await session.close()
    
    return foundPageAddresses


# for importing flags
def getNames(list):
    val = []
    for s in list:
        name = s.split(',')
        for n in name: 
            val.append(n.casefold()) # for case-insensitive comparisons
    return val

# SETUP

# keywords to filter page links 
page_filter = ["service", "ministry", "ministries", "welcome", "contact", "about us", "language", 
               "group", "culture", "home", "history", "translation", "connect", "giving", "global"
               "nation"]
Data = {}
links_list = {}

key_column = "Business Registration Number:"
value_column = "Website:"

with open('data-scrape/data/sample-results.csv', mode='r', newline='', encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile)
    
    # Check if the columns exist
    if key_column not in reader.fieldnames or value_column not in reader.fieldnames:
        raise ValueError(f"Columns {key_column} or {value_column} not found in CSV file")
    
    # Iterate through each row in the CSV file
    for row in reader:
        key = row[key_column]
        value = row[value_column]
        links_list[key] = value
print(links_list.items())

# import flags
temp = pd.read_csv('data-scrape/flags.csv', usecols=[1])["Nation"].to_list()
nation = getNames(temp)
temp = pd.read_csv('data-scrape/flags.csv', usecols=[2])["People"].to_list()
people = getNames(temp)
temp = pd.read_csv('data-scrape/flags.csv', usecols=[3])["Languages"].to_list()
language = getNames(temp)

flags = dict.fromkeys(set(nation + people + language), False)

# find all pages on site
for num, link in links_list.items():
    if link != 'n/a': 
        print(link)
        # create a seperate instance of flags
        myflags = dict.fromkeys(flags, False)

        index_pages = None
        try:
            index_pages = asyncio.run(collectPagesFromMaps("https://" + link))
            link = "https://" + link
        except:
            try:
                index_pages = asyncio.run(collectPagesFromMaps("http://" + link))
                link = "http://" + link
            except:
                try:
                    index_pages = asyncio.run(collectPagesFromMaps(link))
                except:
                    pass
        print("INDEX PAGES")
        print(index_pages)

        if index_pages != None:

            # filter out relevant links
            pages = []
            # link_length = re.compile('(.*://.*/.*)/')
            for page in index_pages:
                # validate link
                if validators.url(page):
                    # format the link - make sure link ends with slash
                    if page[-1] != '/':
                        page += '/'
                    # only keep links of a certain length
                    #if link_length.match(page) is not None:
                    test = page.count('/')
                    if test <=4:
                        pages.append(page)

            # extra filtering if too many links
            if len(pages) > 20:
                temp = pages
                pages = []
                for page in temp:
                    if any(ele in page for ele in page_filter):
                        pages.append(page)

            # quicksolve of incomplete sitemaps
            if len(pages) == 0:
                pages.append(link)
                            
            print(len(pages))
            # scan relevant links for information
            print("PAGES")
            print(pages)

            for page in pages: 
                print(page)
                site_content = urllib.request.urlopen(page).read().decode("utf-8")
                for word in myflags:
                    if word in site_content.casefold():
                        myflags[word] = True

        # TODO: deal with sitemap location failure

        Data[num] = myflags

with open('language-data.json', 'w') as fp:
    json.dump(Data, fp)