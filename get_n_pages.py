import requests
import parse_ads_basics as pbb
from datetime import datetime
from bs4 import BeautifulSoup
import os
import codecs
import string
import platform
import re
import time
import json
import math
import csv


def gnp_nettivene(html='n'):
    if html == 'n':
        url = "https://www.nettivene.com/en/purjevene"
        r = pbb.get_html_from_url(url)
    else:
        r = html
    soup = BeautifulSoup(r, 'lxml')
    # print(soup.get_text())
    n_page = int(soup.find("span", class_="totPage").text)
    return n_page


def gnp_blocket(html='n'):
    if html == 'n':
        url = "https://www.blocket.se/annonser/hela_sverige/fordon/batar/segelbat?cg=1062&q=segelb%C3%A5t"
        r = pbb.get_html_from_url(url)
    else:
        r = html
        # r = pbb.load_html_file('2020.07.22_15.39.19.html')

    soup = BeautifulSoup(r, 'lxml')
    script = soup.find_all('a', href=True)
    print('\n\n\n\n\n\n')
    n_page = 0
    for link in script:
        useful_link = link['href'].find('page=')
        if useful_link != -1:
            text = link['href'][useful_link+5:useful_link+10].split('&')[0]
            if int(text) > n_page:
                n_page = int(text)
    print('Blocket n_page: ', n_page)
    return n_page


def gnp_finn_no(html='n'):
    if html == 'n':
        url = "https://www.finn.no/boat/forsale/search.html?class=2188&sort=PUBLISHED_DESC"
        r = pbb.get_html_from_url(url)
    else:
        r = html
        # r = pbb.load_html_file('2020.07.22_15.39.19.html')

    soup = BeautifulSoup(r, 'lxml')
    script = soup.find_all(True, {'class': ['u-strong']})
    n_boat = script[0].text
    n_page = int(n_boat) // 50 + 1
    print('Finn.no boats total:', n_boat)
    return n_page, n_boat
