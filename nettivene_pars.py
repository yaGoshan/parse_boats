import requests
import parse_ads_basics as pab
import get_n_pages as gnp
from datetime import datetime
from bs4 import BeautifulSoup
import get_n_pages as gnp
import os
import codecs
import string
import platform
import re
import time
import csv



def load_boat_by_link_nettivene(url=''):
    if url == '':
        url = "https://www.nettivene.com/en/purjevene/finn/806118"

    r = pab.get_html_from_url(url)
    soup = BeautifulSoup(r, 'lxml')
    print(url)
    idb = soup.find('span', {'itemprop': 'productID'}).get_text().split('.')[0]
    bmodel = soup.find('h1').find('a', {'itemprop': 'url'})['title']. \
        replace(' ', '_').replace('/', '')

    print(idb)
    print(bmodel)

    test = False
    if not test:
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


def parse_links_from_nettivene():
    """ Parses links to boat pages boat names and prices. """
    site = 'nettivene'
    url_base = "https://www.nettivene.com/en/purjevene?sortCol=enrolldate&ord=DESC&page={}"
    result = list()
    for i in range(1, gnp.get_p_and_b(site)[0] + 1):
    # for i in range(1, 3):
        url = url_base.format(str(i))
        print(url)
        html = pab.get_html_from_url(url)
        boats = extract_ads_nettivene(html)
        for i in boats:
            print(i)
        print(boats)
        result = result + boats
    # print(result)
    name = 'nettivene_boat_links_' + str(datetime.now().strftime("%Y.%m.%d_%H.%M.%S"))
    with open(os.getcwd() + '/nettivene_boat_links/' + name + '.csv', 'w') as csv_file:
        writer = csv.writer(csv_file, delimiter=';')
        for boat in result:
            writer.writerow(boat)
    print("Boats total: " + str(len(result)))


def load_all_new_boats_nettivene():
    i = 0
    links = diff_parse_links(mode='d')
    for link in links:
        i = i + 1
        load_boat_by_link_nettivene(link)
        print("Made: " + str(i) + ' Out of: ' + str(len(links)))
        print('')
        time.sleep(3)


if __name__ == "__main__":
    # print(gnp.gnp_nettivene())
    # pab.save_html_file("https://www.nettivene.com/en/purjevene?sortCol=enrolldate&ord=DESC&page=1", '123')
    # html = pab.load_html_file('html/123_2021.03.06_21.51.48.html')
    # for i in extract_ads_nettivene(html):
    #     print(i)
    # input()
    # load_boat_by_link_nettivene()

    parse_links_from_nettivene()
    print(pab.diff_parse_links(site='nettivene', mode='d'))

    # load_all_new_boats_nettivene()
