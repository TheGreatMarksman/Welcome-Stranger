import pandas as pd
import requests
import re
from urllib.parse import urlparse, urljoin
from urllib.robotparser import RobotFileParser
from bs4 import BeautifulSoup
import math

FILENAME = 'data/test-results-1000.csv'
OUTPUT_FILE = 'data/contact-info-results-1000.csv'

def find_phones(text):
    return re.findall(r'\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}', text)

def find_emails(text):
    return re.findall(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', text)
    
def find_contact_page(soup):
    return soup.find('a', href=True, string=re.compile(r'contact', re.I))

def find_about_page(soup):
    return soup.find('a', href=True, string=re.compile(r'about', re.I))

def fetch_contact_info(url):        
    print(f"  Finding Info For {url}")
    contact_info = {'email':'N/A', 'phone': 'N/A'}
    
    robot_url = url + '/robots.txt'
    rp = RobotFileParser()
    rp.set_url(robot_url)
    rp.read()

    response = requests.get(url)
    if not response.ok: return contact_info
    if not rp.can_fetch("*", url):
        print("Robots restricted")
        return contact_info

    
    soup = BeautifulSoup(response.content, 'html.parser')
    
    contact_info['emails'] = find_emails(soup.text)
    contact_info['phones'] = find_phones(soup.text)
    
    contact_page = find_contact_page(soup)
    about_page = find_about_page(soup)
    found_contact_page = False
    if contact_page:
        print("  Searching Contact Page")
        contact_url = contact_page['href']
        if not contact_url.startswith('http'):
            contact_url = url + contact_url
        contact_response = requests.get(contact_url)
        if contact_response.ok:
            found_contact_page = True
            contact_soup = BeautifulSoup(contact_response.content, 'html.parser')
            contact_info['contact_page_emails'] = find_emails(contact_soup.text)
            contact_info['contact_page_phones'] = find_phones(contact_soup.text)
            
    
    if not found_contact_page and about_page:
        print("  Searching About Page")
        about_url = about_page['href']
        if not about_url.startswith('http'):
            about_url = url + about_url
        about_response = requests.get(about_url)
        if about_response.ok:
            about_soup = BeautifulSoup(about_response.content, 'html.parser')
            contact_info['about_page_emails'] = find_emails(about_soup.text)
            contact_info['about_page_phones'] = find_phones(about_soup.text)
        
    if 'contact_page_emails' in contact_info and contact_info['contact_page_emails']:
        contact_info['email'] = contact_info['contact_page_emails'][0]
    elif contact_info['emails']:
        contact_info['email'] = contact_info['emails'][0]
    elif 'about_page_emails' in contact_info and contact_info['about_page_emails']:
        contact_info['email'] = contact_info['about_page_emails'][0]
    else:
        contact_info['email'] = 'N/A'
        
    if 'contact_page_phones' in contact_info and contact_info['contact_page_phones']:
        contact_info['phone'] = contact_info['contact_page_phones'][0]
    elif 'phones' in contact_info['phones']:
        contact_info['phone'] = contact_info['phones'][0]
    if 'about_page_phones' in contact_info and contact_info['about_page_phones']:
        contact_info['phone'] = contact_info['about_page_phones'][0]
    else:
        contact_info['phone'] = 'N/A'
    return contact_info
    
# URL = "https://www.lwchurch.ca"
# contact_info = fetch_contact_info(URL)
# print(contact_info['email'])
# print(contact_info['phone'])

sites = pd.read_csv(FILENAME, usecols=['Business Registration Number:','Website:'])
sites['email'] = 'N/A'
sites['phone'] = 'N/A'

def fetch_from_site(site):
    print(f"Processing #{site.name}")
    if isinstance(site['Website:'], float): return site
    
    url = site['Website:'].lower()
    
    contact_info = {'email':'N/A', 'phone': 'N/A'}
    if not url.startswith('http'):
        try:
            contact_info = fetch_contact_info('https://' + url)
        except Exception:
            try: 
                contact_info = fetch_contact_info('http://' + url)
            except Exception:
                print("  - Could not get info")
    else:
        try:
            contact_info = fetch_contact_info('http://' + url)
        except Exception:
            print("  - Could not get info")

            
    site['email'] = contact_info['email']
    site['phone'] = contact_info['phone']
    return site

sites = sites.apply(fetch_from_site, axis=1)

sites.to_csv(OUTPUT_FILE, index=False, encoding='utf-8')