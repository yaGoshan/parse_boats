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
import extract_parse_save as eps


def load_boat_by_link_blocket(url=''):
    if url == '':
        url = "https://www.blocket.com/en/purjevene/finn/806118"

    r = pab.get_html_from_url(url)
    soup = BeautifulSoup(r, 'lxml')
    print(url)
    idb = soup.find('span', {'itemprop': 'productID'}).get_text().split('.')[0]
    bmodel = soup.find('h1').find('a', {'itemprop': 'url'})['title']. \
        replace(' ', '_').replace('/', '')

    print(idb)
    print(bmodel)

    test = False
    if test != True:
        name = bmodel + '/' + str(datetime.now().strftime("%Y.%m.%d_%H.%M.%S")) + '_' + idb
        path_to_folder = pab.get_path('boat_pages') + name
        # os.makedirs(pab.get_path('boat_pages')+bmodel, exist_ok=True)
        os.makedirs(path_to_folder, exist_ok=True)

        """ Writes down an html of the boat """
        with open(
                path_to_folder + '/' + bmodel + '_' + idb + str(datetime.now().strftime("%Y.%m.%d_%H.%M.%S")) + '.html',
                'w') as output:
            output.write(r)

        jpgs = soup.find_all('a', href=True)
        # print(jpgs)
        n_pics = 0
        for a in jpgs:
            if a['href'][-9:] == 'large.jpg':
                pab.load_image_from_url(a['href'], path_to_folder)
                n_pics = n_pics + 1
                # print(a['href'])
        print("There " + str(n_pics) + ' pics.')


def parse_links_blocket():
    """ Parses links to boat pages, boat names and prices. """
    site = 'blocket'
    url_base = "https://www.blocket.se/annonser/hela_sverige/fordon/batar/segelbat?cg=1062&page={}&q=segelb%C3%A5t"
    result = list()
    try:
        for i in range(1, gnp.get_p_and_b(site)[0] + 1):
        # for i in range(9, 10):
            url = url_base.format(str(i))
            print(url)
            r = pab.get_html_from_url(url)
            soup = BeautifulSoup(r, 'lxml')

            """ R1 - boat names. R2 - boat price  R3 - boat links"""
            boats = []

            for EachPart in soup.select('a[class*="Link-sc-6wulv7-0 styled__StyledTitleLink-sc-1kpvi4z-10 enigRj"]'):
                # print(EachPart.get_text(), EachPart['href'], type(EachPart))
                boats.append([EachPart.get_text(), 'https://www.blocket.se' + EachPart['href']])

            for idx, EachPart in enumerate(soup.select('div[class*="Price__StyledPrice-sc-1v2maoc-1 jkvRCw"]')):
                # print(EachPart.get_text())
                price = EachPart.get_text().replace(' ', '').replace('kr', '')
                if len(price) == 0:
                    price = -1
                if idx < len(boats):
                    boats[idx].append(price)
                else:
                    print(price)

            for boat in boats:
                print(boat)
            result += boats
            # input()
            # r1 = soup.find_all('span', class_='styled__SubjectContainer-sc-1kpvi4z-11 jzzuDW')
            # r2 = soup.find_all('div', class_='Price__StyledPrice-sc-1v2maoc-1 jkvRCw')
            # r3 = soup.find_all('a', class_='Link-sc-139ww1j-0 styled__StyledTitleLink-sc-1kpvi4z-10 enigRj')
            # print(r1, r2, r3, sep='\n')
            # for i in range(len(r1)):
            #     # print([r1[i].get_text(),r3[i]['href'],r2[i].get_text()])
            #     bname = r1[i].get_text().replace('|', '').replace('\\', '').replace('/', '').replace(';', '')
            #     if r2[i].get_text().replace(' ', '') == '':
            #         price = '-1'
            #     else:
            #         price = r2[i].get_text().replace(' ', '').replace('kr', '')
            #     result.append([bname, 'https://www.blocket.se' + r3[i]['href'], price])

        # print(result)
    finally:
        name = 'blocket_boat_links_' + str(datetime.now().strftime("%Y.%m.%d_%H.%M.%S"))
        with open(os.getcwd() + '/blocket_boat_links/' + name + '.csv', 'w') as csv_file:
            writer = csv.writer(csv_file, delimiter=';')
            for boat in result:
                writer.writerow(boat)
        print("Boats total: " + str(len(result)))


def load_all_new_boats_blocket():
    i = 0
    links = diff_parse_links(mode='d')
    for link in links:
        i = i + 1
        load_boat_by_link_blocker(link)
        print("Made: " + str(i) + ' Out of: ' + str(len(links)))
        print('')
        time.sleep(3)


if __name__ == "__main__":
    eps.load_and_save('blocket')
    pab.diff_parse_links(site='blocket', mode='d', offset=0)
    # load_boat_by_link_blocker()
    # load_all_new_boats_blocket()
    # load_boat_by_link_blocker()
    # parse_links_from_blocket()
