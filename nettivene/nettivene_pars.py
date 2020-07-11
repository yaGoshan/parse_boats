import requests
from datetime import datetime
from bs4 import BeautifulSoup
import os
import codecs
import string
import platform


def get_n_pages(html='n'):
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
    c_os = platform.system()
    if c_os == "Windows":
        path_to_file = os.getcwd() + '\\boat_links\\' + file_name
    else:
        path_to_file = os.getcwd() + '/boat_links/' + file_name

    with open(path_to_file, 'r') as handler:
        r = handler.readlines()
    res = [[], [], []]
    for boat in r:
        buff = boat.split('|')
        buff[2] = buff[2].replace(' ', '')[:-2]
        buff[2] = buff[2][:-2]
        if buff[2] == 'Notpri':
            buff[2] = -1
        else:
            buff[2] = int(buff[2])
        for i in range(3): res[i].append(buff[i])
    return res


def load_image_from_url_nettivene(url, model, idb):
    img_data = requests.get(url).content
    os.makedirs(os.getcwd() + r'/boat_pages/' + model + r'/' + idb, exist_ok=True)
    pic_name = os.getcwd() + r'/boat_pages/' + model + r'/' + idb + r'/' + url.split('/')[-1]
    with open(pic_name, 'wb') as handler:
        handler.write(img_data)


def parse_boat_by_link():
    url = "https://www.nettivene.com/en/purjevene/albin/754843"
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'lxml')
    jpgs = soup.find_all('a', href=True)
    # print(jpgs)
    idx = soup.find('span', {'itemprop': 'productID'})
    print(idx.get_text().split('.')[0])

    model = 'albin57'
    idb = '456879'

    for a in jpgs:
        if a['href'][-9:] == 'large.jpg':
            load_image_from_url_nettivene(a['href'], model, idb)
            print(a['href'])

    # name = 'boat_page_' + str(datetime.now().strftime("%Y.%m.%d_%H:%M:%S"))
    # with open(os.getcwd() + '/boat_pages/' + name + '.html', 'w') as output:
    #     output.write(r.text)


def diff_parse_links():
    c_os = platform.system()
    if c_os == "Windows":
        path_to_parse = os.getcwd() + '\\boat_links\\'
    else:
        path_to_parse = os.getcwd() + '/boat_links/'
    files_list = []
    for file in os.listdir(path_to_parse):
        if file.endswith(".txt"):
            # print(os.path.join(os.getcwd(), file))
            files_list.append([file, os.path.getctime(path_to_parse + file)])

    # TODO: check is sort working
    print(files_list)
    files_list.sort(key=lambda x: x[1])
    print(files_list)
    for file in files_list:
        print(file)

    boat_table_new = read_links_from_file(files_list[-1][0])
    links_new = boat_table_new[1]

    boat_table_old = read_links_from_file(files_list[-2][0])
    links_old = boat_table_old[1]

    new_s = set(links_new)
    old_s = set(links_old)
    sold_boats = [x for x in old_s if x not in new_s]
    new_boats = [x for x in new_s if x not in old_s]
    still_boats = [x for x in new_s if x in old_s]

    print("New boats: " + str(len(new_boats)),
          "Boats sold: " + str(len(sold_boats)),
          "Boats still: " + str(len(still_boats)), sep='\n', end='\n\n\n')

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

def parse_links_from_nettivene():
    """ Parses links to boat pages boat names and prices. """
    url_base = "https://www.nettivene.com/en/purjevene?sortCol=enrolldate&ord=DESC&page={}"
    result = list()
    for i in range(1, get_n_pages() + 1):
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


if __name__ == "__main__":
    diff_parse_links()
    # diff_parse_links()
