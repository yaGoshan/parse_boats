import requests
import parse_ads_basics as pab
import boat_parser_additional_functions as bp_af
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


def parse_links_finn_no():
    """ Parses links to boat names, boat pages, prices(Norway krone) and year. """
    url_base = "https://www.finn.no/boat/forsale/search.html?class=2188&page={}&sort=PUBLISHED_DESC"
    result = list()
    try:
        for i in range(1, gnp.gnp_finn_no()[0] + 1):
        # for i in range(1, 2):
            url = url_base.format(str(i))
            print(url)
            r = pab.get_html_from_url(url)
            boats = extract_ads_finn_no(r)
            for boat in boats:
                print(boat)
            print()
            result += boats
    finally:
        name = 'finn_no_boat_links_' + str(datetime.now().strftime("%Y.%m.%d_%H.%M.%S"))
        with open(os.getcwd() + '/finn_no_boat_links/' + name + '.csv', 'w') as csv_file:
            writer = csv.writer(csv_file, delimiter=';')
            for boat in result:
                writer.writerow(boat)
        print("Boats total: " + str(len(result)))


if __name__ == "__main__":
    # parse_links_finn_no()
    pab.diff_parse_links('finn_no', 'd')

    # print(html)
    # html = pab.load_html_file('html/123_2021.03.06_13.07.43.html')
    # for i in extract_ads_finn_no(html):
    #     print(i)
    # pab.save_html_file("https://www.finn.no/boat/forsale/search.html?class=2188&page=1&sort=PUBLISHED_DESC", '123')
