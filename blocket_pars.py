import requests
import parse_boat_basics as pbb
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


def get_n_pages_blocket(html='n'):
    if html == 'n':
        url = "https://www.blocket.se/annonser/hela_sverige/fordon/batar/segelbat?cg=1062&q=segelb%C3%A5t"
        r = requests.get(url)
    else:
        r = html
        # r = pbb.load_html_file('2020.07.22_15.39.19.html')
    soup = BeautifulSoup(r.text, 'lxml')
    # print('Hi!!', soup.find('script', {'id': 'initialState'}).get_text)
    # script = soup.find('script', {'id': 'initialState'}).text
    script = soup.find('script', {'id': 'initialState'}).string
    data = json.loads(script)
    n_page = math.ceil(data['classified']['searchResultCountPreview']['searchTotal'] / 40)
    return n_page


def load_boat_by_link_blocker(url=''):
    if url == '':
        url = "https://www.blocket.com/en/purjevene/finn/806118"

    r = requests.get(url).text
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
        path_to_folder = pbb.get_path('boat_pages') + name
        # os.makedirs(pbb.get_path('boat_pages')+bmodel, exist_ok=True)
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
                pbb.load_image_from_url(a['href'], path_to_folder)
                n_pics = n_pics + 1
                # print(a['href'])
        print("There " + str(n_pics) + ' pics.')


def parse_links_from_blocket():
    """ Parses links to boat pages boat names and prices. """
    url_base = "https://www.blocket.se/annonser/hela_sverige/fordon/batar/segelbat?cg=1062&page={}&q=segelb%C3%A5t"
    result = list()
    for i in range(1, get_n_pages_blocket() + 1):
    # for i in range(1, 2):
        url = url_base.format(str(i))
        print(url)
        r = requests.get(url)
        soup = BeautifulSoup(r.text, 'lxml')

        """ R1 - boat names. R2 - boat price  R3 - boat links"""
        r1 = soup.find_all('span', class_='styled__SubjectContainer-sc-1kpvi4z-11 jzzuDW')
        r2 = soup.find_all('div', class_='Price__StyledPrice-sc-1v2maoc-1 jkvRCw')
        r3 = soup.find_all('a', class_='Link-sc-139ww1j-0 styled__StyledTitleLink-sc-1kpvi4z-10 enigRj')
        # print(r1, r2, r3, sep='\n')
        for i in range(len(r1)):
            # print([r1[i].get_text(),r3[i]['href'],r2[i].get_text()])
            bname = r1[i].get_text().replace('|', '').replace('\\', '').replace('/', '').replace(';', '')
            if r2[i].get_text().replace(' ', '') == '':
                price = '-1'
            else:
                price = r2[i].get_text().replace(' ', '').replace('kr', '')
            result.append([bname, 'https://www.blocket.se' + r3[i]['href'], price])

    # print(result)
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
    parse_links_from_blocket()
    pbb.diff_parse_links(site='blocket', mode='d')
    # load_boat_by_link_blocker()
    # load_all_new_boats_blocket()
    # load_boat_by_link_blocker()
    # parse_links_from_blocket()
