import requests
from datetime import datetime
from bs4 import BeautifulSoup
import os
import codecs
import string
import platform
import re
import time
import csv


def get_path(subfolder=''):
    c_os = platform.system()
    if c_os == "Windows":
        path_to_parse = os.getcwd() + '\\' + subfolder + '\\'
    else:
        path_to_parse = os.getcwd() + '/' + subfolder + '/'
    return path_to_parse


def load_image_from_url(url, path):
    """ Function loads image from URL and saves to path """
    img_data = requests.get(url).content
    pic_name = path + '/' + url.split('/')[-1]
    with open(pic_name, 'wb') as handler:
        handler.write(img_data)


def read_links_from_file(file_name, site):
    """ Function returning [[boat names], [links], [prices]] """
    path_to_file = get_path(site + '_' + 'boat_links') + file_name

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


def diff_parse_links(site, mode='', offset=0):
    """
    Function returns links to boats depends on a mode.
    Modes:
    a -from old and new files
    d - only new if comparing lates file
    l - lates file
    """
    path_to_parse = get_path(site + '_boat_links')
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
    boat_table_new = read_links_from_file(files_list[-1 - offset][0], site)
    links_new = boat_table_new[1]
    print('New file: ' + files_list[-1 - offset][0])

    boat_table_old = read_links_from_file(files_list[-2 - offset][0], site)
    links_old = boat_table_old[1]
    print('Old file: ' + files_list[-2 - offset][0] + '\n')

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

def save_html_file(url):
    r = requests.get(url).text
    with open(pbb.get_path() + str(datetime.now().strftime("%Y.%m.%d_%H.%M.%S")) + '.html',
              'w') as output:
        output.write(r)


def load_html_file(name):
    text = ''
    with open(get_path() + name,
              'r') as output:
        text = output.read()
    return text
