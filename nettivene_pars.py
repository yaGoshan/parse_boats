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
import csv


def get_n_pages_nettivene(html='n'):
    if html == 'n':
        url = "https://www.nettivene.com/en/purjevene"
        r = requests.get(url)
    else:
        r = html
    soup = BeautifulSoup(r.text, 'lxml')
    n_page = int(soup.find("span", class_="totPage").text)
    return n_page



def load_boat_by_link(url=''):
    if url == '':
        url = "https://www.nettivene.com/en/purjevene/finn/806118"

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



def parse_links_from_nettivene():
    """ Parses links to boat pages boat names and prices. """
    url_base = "https://www.nettivene.com/en/purjevene?sortCol=enrolldate&ord=DESC&page={}"
    result = list()
    # for i in range(1, get_n_pages_nettivene() + 1):
    for i in range(1, 3):
        url = url_base.format(str(i))
        print(url)
        r = requests.get(url)
        soup = BeautifulSoup(r.text, 'lxml')

        """ R1 - links to boat page. R2 - boat price """
        r1 = soup.find_all('a', class_='childVifUrl tricky_link')
        r2 = soup.find_all('div', class_='main_price')

        for b in r1:
            result.append([b.get_text().strip(), b['href']])
            # print(b.get_text())
            # print(b['href'])
        l_res = len(result) - len(r2)
        for idx, b in enumerate(r2):
            # print(b.get_text())
            if b == 'Notpriced':
                result[l_res + idx].append('-1')
            else:
                result[l_res + idx].append(b.get_text().replace(' ', '').replace('€', ''))
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
        load_boat_by_link(link)
        print("Made: " + str(i) + ' Out of: ' + str(len(links)))
        print('')
        time.sleep(3)


if __name__ == "__main__":
    # load_boat_by_link()
    # parse_links_from_nettivene()
    pbb.diff_parse_links(site='nettivene', mode='d')
    # load_all_new_boats_nettivene()
