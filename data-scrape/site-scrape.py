# filter out names with unwanted words
# split into two databases -> those with websites and those without
# search for keywords for those with websites and tag -> if broken link, move to no website
# somehow deal with those without websites -> google search???
import pandas as pd
import urllib.request
import asyncio, aiohttp, re, gzip

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
            val.append(n)
    return val

# keywords to filter page links 
page_filter = ["service", "ministry", "ministries", "welcome", "contact", "about us", "language", 
               "group", "culture", "home", "our history", "translation", "connect", "ilm"]

# import flags
temp = pd.read_csv('data-scrape/flags.csv', usecols=[1])["Nation"].to_list()
nation = getNames(temp)
temp = pd.read_csv('data-scrape/flags.csv', usecols=[2])["People"].to_list()
people = getNames(temp)
temp = pd.read_csv('data-scrape/flags.csv', usecols=[3])["Languages"].to_list()
language = getNames(temp)

flags = dict.fromkeys(set(nation + people + language), False)

# find all pages on site
link = "https://willingdon.org"
index_pages = asyncio.run(collectPagesFromMaps(link))
# TODO: check for sitemap location failure

# filter out relevant links
pages = []
for page in index_pages:
    if any(ele in page for ele in page_filter):
        pages.append(page)

# scan relevant links for information
print(pages)
for page in pages: 
    site_content = urllib.request.urlopen(page).read().decode("utf-8")

    for word in flags:
        if word in site_content:
            flags[word] = True

print(flags)