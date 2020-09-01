import requests
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


def save_html_file(url):
    r = requests.get(url).text
    with open(get_path() + str(datetime.now().strftime("%Y.%m.%d_%H.%M.%S")) + '.html',
              'w') as output:
        output.write(r)


def load_html_file(name):
    text = ''
    with open(get_path() + name,
              'r') as output:
        text = output.read()
    return text


def get_path(subfolder=''):
    c_os = platform.system()
    if subfolder != '':
        if c_os == "Windows":
            path_to_parse = os.getcwd() + '\\' + subfolder + '\\'
        else:
            path_to_parse = os.getcwd() + '/' + subfolder + '/'
    else:
        path_to_parse = os.getcwd() + '/'
    return path_to_parse


def get_n_pages_blocket(html='n'):
    if html == 'n':
        url = "https://www.blocket.se/annonser/hela_sverige/fordon/batar/segelbat?cg=1062&q=segelb%C3%A5t"
        r = requests.get(url)
    else:
        r = html
    r = load_html_file('2020.07.22_15.39.19.html')
    soup = BeautifulSoup(r, 'lxml')
    # print('Hi!!', soup.find('script', {'id': 'initialState'}).get_text)
    # script = soup.find('script', {'id': 'initialState'}).text
    script = soup.find('script', {'id': 'initialState'}).string
    data = json.loads(script)
    n_page = math.ceil(data['classified']['searchResultCountPreview']['searchTotal'] / 40)
    return n_page


def read_links_from_file(file_name):
    """ Function returning [[boat names], [links], [prices]] """
    path_to_file = get_path('boat_links') + file_name

    with open(path_to_file, 'r') as csv_file:
        r = csv.reader(csv_file, delimiter=';')
        res = [[], [], []]
        for boat in r:
            # print(boat)
            if boat[2] == '':
                boat[2] = -1
            else:
                boat[2] = int(boat[2])
            for i in range(3):
                res[i].append(boat[i])
    return res


def load_image_from_url(url, path):
    """ Function loads image from URL and saves to path """
    img_data = requests.get(url).content
    pic_name = path + '/' + url.split('/')[-1]
    with open(pic_name, 'wb') as handler:
        handler.write(img_data)


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
        path_to_folder = get_path('boat_pages') + name
        # os.makedirs(get_path('boat_pages')+bmodel, exist_ok=True)
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
                load_image_from_url(a['href'], path_to_folder)
                n_pics = n_pics + 1
                # print(a['href'])
        print("There " + str(n_pics) + ' pics.')


def diff_parse_links(mode='', offset=0):
    """
    Function returns links to boats depends on a mode.
    Modes:
    a -from old and new files
    d - only new if comparing lates file
    l - lates file
    """
    path_to_parse = get_path('boat_links')
    files_list = []
    for file in os.listdir(path_to_parse):
        if file.endswith(".csv"):
            # print(os.path.join(os.getcwd(), file))
            # print(file)
            files_list.append([file, os.path.getctime(path_to_parse + file)])

    # for file in files_list:
    #     print(file)
    # print('')
    files_list.sort(key=lambda x: x[0])
    # for file in files_list:
    #     print(file)

    """ Offsets file selection to past. 0 - newest and next after it """
    print('New file: ' + files_list[-1 - offset][0])
    boat_table_new = read_links_from_file(files_list[-1 - offset][0])
    links_new = boat_table_new[1]

    print('Old file: ' + files_list[-2 - offset][0] + '\n')
    boat_table_old = read_links_from_file(files_list[-2 - offset][0])
    links_old = boat_table_old[1]

    new_s = set(links_new)
    old_s = set(links_old)
    sold_boats = [x for x in old_s if x not in new_s]
    new_boats = [x for x in new_s if x not in old_s]
    still_boats = [x for x in new_s if x in old_s]

    print("Boats used to be:" + str(len(old_s)),
          "Boats now:" + str(len(new_s)),
          "New boats: " + str(len(new_boats)),
          "Boats sold: " + str(len(sold_boats)),
          "Boats still: " + str(len(still_boats)), sep='\n', end='\n\n')

    for boat in still_boats:
        price_old = -1
        price_new = -1
        name_b = ''
        for x in range(len(boat_table_old[1])):
            if boat == boat_table_old[1][x]:
                price_old = boat_table_old[2][x]
                name_b = boat_table_old[0][x]
        for x in range(len(boat_table_new[1])):
            if boat == boat_table_new[1][x]:
                price_new = boat_table_new[2][x]
        if price_new != price_old:
            print(name_b, price_new, price_old, sep=' ', end='\n')
    print('\n\n')
    # for b_name in boat_table_new[0]:
    #     new_b_name = b_name.replace('/','')
    #     # print(new_b_name)
    #     if new_b_name != b_name:
    #         print(b_name + '     ' + new_b_name)
    if mode == 'a':
        print('Mode not working.')
    if mode == 'd':
        return new_boats
    if mode == 'l':
        return new_s


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
            result.append([bname,
                           'https://www.blocket.se' + r3[i]['href'], r2[i].get_text().replace(' ', '').replace('kr', '')] )

    # print(result)
    name = 'blocket_boat_links_' + str(datetime.now().strftime("%Y.%m.%d_%H.%M.%S"))
    with open(os.getcwd() + '/boat_links/' + name + '.csv', 'w') as csv_file:
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
    # save_html_file('https://www.blocket.se/annonser/hela_sverige/fordon/batar/segelbat?cg=1062&page=1&q=segelb%C3%A5t')
    parse_links_from_blocket()
    diff_parse_links(mode='d')
    # load_boat_by_link()
    # load_all_new_boats_nettivene()
    # load_boat_by_link()
    # parse_links_from_nettivene()
