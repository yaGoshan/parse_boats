import requests
from datetime import datetime
from bs4 import BeautifulSoup
import os
import codecs
import string
import platform
import re
import time


def get_path(subfolder=''):
    c_os = platform.system()
    if c_os == "Windows":
        path_to_parse = os.getcwd() + '\\' + subfolder + '\\'
    else:
        path_to_parse = os.getcwd() + '/' + subfolder + '/'
    return path_to_parse


def get_n_pages_nettivene(html='n'):
    if html == 'n':
        url = "https://www.nettivene.com/en/purjevene"
        r = requests.get(url)
    else:
        r = html
    soup = BeautifulSoup(r.text, 'lxml')
    n_page = int(soup.find("span", class_="totPage").text)
    return n_page


def read_links_from_file(file_name):
    """ Function returning [[boat names], [links], [prices]] """
    path_to_file = get_path('boat_links') + file_name

    with open(path_to_file, 'r') as handler:
        r = handler.readlines()
    res = [[], [], []]
    for boat in r:
        buff = boat.split('|')
        buff[2] = buff[2].replace(' ', '')[:-2]
        if buff[2] == 'Notprice':
            buff[2] = -1
        else:
            buff[2] = int(buff[2])
        for i in range(3): res[i].append(buff[i])
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
    bmodel = soup.find('h1').find('a', {'itemprop':'url'})['title'].\
        replace(' ','_').replace('/','')

    print(idb)
    print(bmodel)

    test = False
    if test != True:
        name = bmodel + '/' + str(datetime.now().strftime("%Y.%m.%d_%H.%M.%S")) + '_' + idb
        path_to_folder = get_path('boat_pages')+name
        # os.makedirs(get_path('boat_pages')+bmodel, exist_ok=True)
        os.makedirs(path_to_folder, exist_ok=True)

        """ Writes down an html of the boat """
        with open(path_to_folder + '/' + bmodel + '_' + idb +  str(datetime.now().strftime("%Y.%m.%d_%H.%M.%S")) + '.html', 'w') as output:
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


def diff_parse_links(mode = '', offset = 0):
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
        if file.endswith(".txt"):
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
    boat_table_new = read_links_from_file(files_list[-1-offset][0])
    links_new = boat_table_new[1]
    print('New file: ' + files_list[-1 - offset][0])

    boat_table_old = read_links_from_file(files_list[-2-offset][0])
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


def parse_links_from_nettivene():
    """ Parses links to boat pages boat names and prices. """
    url_base = "https://www.nettivene.com/en/purjevene?sortCol=enrolldate&ord=DESC&page={}"
    result = list()
    for i in range(1, get_n_pages_nettivene() + 1):
        url = url_base.format(str(i))
        print(url)
        r = requests.get(url)
        soup = BeautifulSoup(r.text, 'lxml')

        """ R1 - links to boat page. R2 - boat price """
        r1 = soup.find_all('a', class_='childVifUrl tricky_link')
        r2 = soup.find_all('div', class_='main_price')

        for b in r1:
            result.append([b.get_text(), b['href']])
            # print(b.get_text())
            # print(b['href'])
        l_res = len(result) - len(r2)
        for idx, b in enumerate(r2):
            # print(b.get_text())
            result[l_res + idx].append(b.get_text())
    # print(result)
    name = 'nettivene_boat_links_' + str(datetime.now().strftime("%Y.%m.%d_%H.%M.%S"))
    with open(os.getcwd() + '/boat_links/' + name + '.txt', 'w') as output:
        for boat in result:
            res = '|'.join(boat) + '\n'
            output.write(res)
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
    # diff_parse_links(mode='d')
    # load_boat_by_link()
    # parse_links_from_nettivene()
    # print(diff_parse_links(mode='d'))
    load_all_new_boats_nettivene()

