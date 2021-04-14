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

links_n_page = {'nettivene': 'https://www.nettivene.com/en/purjevene', 
              'blocket': "https://www.blocket.se/annonser/hela_sverige/fordon/batar/segelbat?cg=1062&q=segelb%C3%A5t",
              'finn_no': "https://www.finn.no/boat/forsale/search.html?class=2188&sort=PUBLISHED_DESC"}


def nettivene_pab(html):
    soup = BeautifulSoup(html, 'lxml')
    n_boat = int(soup.find(class_='totAdInList').text)
    n_page = int(soup.find("span", class_="totPage").text)
    return n_page, n_boat
    

def blocket_pab(html):
    soup = BeautifulSoup(html, 'lxml')
    script = soup.find_all('a', href=True)
    n_boat = soup.find('div', {'data-cy': 'search-result-count'}).text.split(' ')[0]
    n_page = 0
    for link in script:
        useful_link = link['href'].find('page=')
        if useful_link != -1:
            text = link['href'][useful_link+5:useful_link+10].split('&')[0]
            if int(text) > n_page:
                n_page = int(text)
    return n_page, n_boat


def finn_no_pab(html):
    soup = BeautifulSoup(html, 'lxml')
    script = soup.find_all(True, {'class': ['u-strong']})
    n_boat = script[0].text
    n_page = int(n_boat) // 50 + 1
    return n_page, n_boat
    
    
def get_p_and_b(site, html='n'):
    if html == 'n':
        url = links_n_page[site]
        r = pbb.get_html_from_url(url)
    else:
        r = html

    possibles = globals().copy()
    possibles.update(locals())
    method = possibles.get(site + '_pab')
    n_page, n_boat = method(r)
    print(site + ' boats total: ', n_boat, '\nPages total: ', n_page)
    return n_page, n_boat


#
# def gnp_nettivene(html='n'):
#     site = 'nettivene'
#     if html == 'n':
#         url = "https://www.nettivene.com/en/purjevene"
#         r = pbb.get_html_from_url(url)
#     else:
#         r = html
#     soup = BeautifulSoup(r, 'lxml')
#     n_boat = int(soup.find(class_='totAdInList').text)
#     n_page = int(soup.find("span", class_="totPage").text)
#     print(site + ' boats total: ', n_boat, '\nPages total: ', n_page)
#     return n_page, n_boat
#
#
# def gnp_blocket(html='n'):
#     site = 'blocket'
#     if html == 'n':
#         url = "https://www.blocket.se/annonser/hela_sverige/fordon/batar/segelbat?cg=1062&q=segelb%C3%A5t"
#         r = pbb.get_html_from_url(url)
#     else:
#         r = html
#
#     soup = BeautifulSoup(r, 'lxml')
#     script = soup.find_all('a', href=True)
#     n_boat = soup.find('div', {'data-cy': 'search-result-count'}).text.split(' ')[0]
#     n_page = 0
#     for link in script:
#         useful_link = link['href'].find('page=')
#         if useful_link != -1:
#             text = link['href'][useful_link+5:useful_link+10].split('&')[0]
#             if int(text) > n_page:
#                 n_page = int(text)
#     print(site + ' boats total: ', n_boat, '\nPages total: ', n_page)
#     return n_page, n_boat
#
#
# def gnp_finn_no(html='n'):
#     site = 'finn.no'
#     if html == 'n':
#         url = "https://www.finn.no/boat/forsale/search.html?class=2188&sort=PUBLISHED_DESC"
#         r = pbb.get_html_from_url(url)
#     else:
#         r = html
#         # r = pbb.load_html_file('2020.07.22_15.39.19.html')
#
#     soup = BeautifulSoup(r, 'lxml')
#     script = soup.find_all(True, {'class': ['u-strong']})
#     n_boat = script[0].text
#     n_page = int(n_boat) // 50 + 1
#     print(site + ' boats total: ', n_boat, '\nPages total: ', n_page)
#     return n_page, n_boat


def gnp_sailboat_data():
    """ Old function for parsing from sailboatdata.com """
    url = "https://sailboatdata.com/sailboat"
    r = pab.get_html_from_url(url)
    boat_number = -1
    soup = BeautifulSoup(r, 'lxml')
    texts = soup.find_all('li')
    for text in texts:
        res = text.text.find('sailboats')
        if res != -1:
            boat_number = int(text.text[0:res])
            print("Sailboat_data boats total: ", boat_number)
    return boat_number
