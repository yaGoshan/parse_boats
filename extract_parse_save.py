import requests
import parse_ads_basics as pab
from datetime import datetime
from bs4 import BeautifulSoup
import get_n_pages as gnp
import os
import codecs
import string
import platform
import re
import time
import json
import math
import csv
import unidecode
import extract_parse_save as eps


ads_page_links = {'finn_no': 'https://www.finn.no/boat/forsale/search.html?class=2188&page={}&sort=PUBLISHED_DESC',
                  'blocket': "https://www.blocket.se/annonser/hela_sverige/fordon/batar/segelbat?cg=1062&page={}&q=segelb%C3%A5t",
                  'nettivene': "https://www.nettivene.com/en/purjevene?sortCol=enrolldate&ord=DESC&page={}"}


def load_and_save(site, print_=True):
    """ Parses links to boat names, boat pages, prices(Norway krone) and year. """
    url_base = ads_page_links[site]
    result = list()

    try:
        n_page = gnp.get_p_and_b(site)[0]
        for i in range(1, n_page + 1):
        # for i in range(1, 3):
            url = url_base.format(str(i))
            print('Current page: ', i, 'out of:', n_page)
            r = pab.get_html_from_url(url)
            possibles = globals().copy()
            possibles.update(locals())
            extract = possibles.get('extract_ads_' + site)
            boats = extract(r)
            if print_:
                for boat in boats:
                    print(boat)
            result += boats
    finally:
        name = site + '_boat_links_' + str(datetime.now().strftime("%Y.%m.%d_%H.%M.%S"))
        with open(os.getcwd() + '/' + site + '_boat_links/' + name + '.csv', 'w') as csv_file:
            writer = csv.writer(csv_file, delimiter=';')
            for boat in result:
                writer.writerow(boat)
        print("Boats total: " + str(len(result)))


def extract_ads_finn_no(html):
    soup = BeautifulSoup(html, 'lxml')
    boats = []

    for eachPart in soup.find_all(True, {'class': ['ads__unit__link']}):
        name = eachPart.get_text()
        link = eachPart['href']
        if link[0] == '/':
            link = 'https://www.finn.no' + link
        # print(name)
        # print(link, '\n')
        boats.append([name, link])

    for idx, eachPart in enumerate(soup.find_all('div', {'class': ['ads__unit__content__keys']})):
        text = unidecode.unidecode(str(eachPart.get_text()).replace('fot', ''))
        # print(text)
        year = text[0:4]
        length = text[4:].split(' ')[0]
        # print(text.split(' '))
        price = ''.join(text.split(' ')[1:-1])
        # print(idx, year, length, price, '\n')
        boats[idx] = boats[idx] + [price, year, length]

    return boats


def extract_ads_nettivene(html):
    soup = BeautifulSoup(html, 'lxml')
    boats = []
    r1 = soup.find_all('a', class_='childVifUrl tricky_link')
    r2 = soup.find_all('div', class_='main_price')

    for b in r1:
        boats.append([b.get_text().strip(), b['href']])
        # print(b.get_text())
        # print(b['href'])

    for idx, b in enumerate(r2):
        # print(b.get_text())
        if b.get_text().replace(' ', '') == 'Notpriced':
            boats[idx].append('-1')
        else:
            boats[idx].append(b.get_text().replace(' ', '').replace('€', ''))
    return boats



def extract_ads_blocket(html):
    soup = BeautifulSoup(html, 'lxml')
    """ R1 - boat names. R2 - boat price  R3 - boat links"""
    boats = []
    # print(soup.text)
    for EachPart in soup.select('a[class*="Link-sc-6wulv7-0 styled__StyledTitleLink-sc-1kpvi4z-10 kWpDHB ilOvgj"]'):
        # print(EachPart.get_text(), EachPart['href'], type(EachPart))
        boats.append([EachPart.get_text(), 'https://www.blocket.se' + EachPart['href']])
        # print(EachPart)

    for idx, EachPart in enumerate(soup.select('div[class*="Price__StyledPrice-sc-1v2maoc-1 dmOeSM"]')):
        # print(EachPart.get_text())
        price = EachPart.get_text().replace(' ', '').replace('kr', '')
        if len(price) == 0:
            price = -1
        if idx < len(boats):
            boats[idx].append(price)
        # else:
            # print(price)
    return boats
