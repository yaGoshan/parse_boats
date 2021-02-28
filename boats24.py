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
import csv


def get_n_pages_boats24():
    url = 'https://www.boats24.com/sailboat/#zustand=gebraucht'
    r = pbb.get_html_from_url(url)
    soup = BeautifulSoup(r, 'lxml')
    text = soup.find_all(True, {'class': ['sr-us']})
    n_boats = int(text[0].get_text().split()[0])
    n_pages = int(n_boats/10)+1
    print(n_boats, n_pages)
    return n_pages


def parse_links_from_boats24():
    """ Parses links to boat pages, boat names, prices, location and year built. """
    url_base = 'https://www.boats24.com/sailboat/?page={}#cur=EUR&auswahl=7'
    result = list()
    try:
        for i in range(1, get_n_pages_boats24() + 1):
        # for i in range(1, 4):
            url = url_base.format(str(i))
            print(url)
            r = pbb.get_html_from_url(url)
            soup = BeautifulSoup(r, 'lxml')

            boat = []
            links = []

            refs = soup.find_all(href=True)
            for item in refs:
                if item['href'][0] == '/' and item['href'][-1] == 'l':
                    links.append('https://www.boats24.com' + item['href'])
                    # print(item['href'])

            elements = soup.find_all(True, {'class': ['sr-objektbox-us', 'details_left', 'sr-price']})
            for idx, EachPart in enumerate(elements):
                text = EachPart.get_text()

                if idx % 3 == 0:
                    try:
                        price = int(text.split()[0].replace(',', ''))
                    except Exception:
                        print(text.split())
                        price = text
                    # print('Price: ', price)
                    boat.append(price)

                if idx % 3 == 1:
                    # print('Name: ', text.replace('/', ''))
                    boat.insert(0, links[idx//3])
                    boat.insert(0, text.replace('/', '').replace('  ', ' '))

                if idx % 3 == 2:
                    text_list = text.replace('\n', '').split('·')
                    year = -1
                    for item in text_list:
                        if item.find('Year') != -1 and year == -1:
                            year = item.split()[-1]
                    region = text_list[-1]
                    condition = text_list[-2].replace(' ', '')
                    text_list = [year] + [region] + [condition]

                    # print('Third: ', text_list)
                    boat = boat + text_list
                    result.append(boat)
                    print(boat)
                    boat = []
    finally:
        # print(result)
        # input()

        # print(result)
        name = 'boats24_boat_links_' + str(datetime.now().strftime("%Y.%m.%d_%H.%M.%S"))
        with open(os.getcwd() + '/boats24_boat_links/' + name + '.csv', 'w') as csv_file:
            writer = csv.writer(csv_file, delimiter=';')
            for boat in result:
                writer.writerow(boat)
        print("Boats total: " + str(len(result)))


if __name__ == '__main__':
    # get_n_pages_boats24()
    parse_links_from_boats24()


