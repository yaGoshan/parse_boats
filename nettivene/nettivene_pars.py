import requests
from datetime import datetime
from bs4 import BeautifulSoup
import os
import codecs
import string

def get_n_pages(html = 'n'):
    if html == 'n':
        url = "https://www.nettivene.com/en/purjevene"
        r = requests.get(url)
    else:
        r = html
    soup = BeautifulSoup(r.text, 'lxml')
    n_page = int(soup.find("span", class_ = "totPage").text)
    return n_page

""" Function returning [[boat names], [links], [prices]] """
def read_links_from_file(file_name):
    path_to_file = os.getcwd() + '/boat_links/' + file_name
    with open(path_to_file, 'r') as handler:

        r = handler.readlines()
    res = [[],[],[]]
    for boat in r:
        buff = boat.split('|')
        buff[2] = buff[2].replace(' ','')[:-2]
        if buff[2] == 'Notprice':
            buff[2] = -1
        else:
            buff[2] = int(buff[2])
        for i in range(3): res[i].append(buff[i])
    return res

def load_image_from_url_nettivene(url, model, idb):
    img_data = requests.get(url).content
    os.makedirs(os.getcwd() + r'/boat_pages/' + model + r'/' + idb, exist_ok=True)
    pic_name = os.getcwd() + r'/boat_pages/' + model + r'/' + idb  + r'/' + url.split('/')[-1]
    with open(pic_name, 'wb') as handler:
        handler.write(img_data)

def parse_boat_by_link():
    url = "https://www.nettivene.com/en/purjevene/albin/754843"
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'lxml')
    jpgs = soup.find_all('a',href=True)
    # print(jpgs)
    idx = soup.find('span', {'itemprop':'productID'})
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
    path_to_parse = os.getcwd() + '/boat_links/'
    print(path_to_parse)
    files_list = []
    for file in os.listdir(path_to_parse):
        if file.endswith(".txt"):
            # print(os.path.join(os.getcwd(), file))

            files_list.append([file,os.path.getctime(path_to_parse+file)])

    print(files_list)
    link1 = read_links_from_file(files_list[0][0])[1]
    # link2 = read_links_from_file(files_list[1][0])[1]
    s = set(link1)
    print(len(s), len(link1))



def parse_links_from_nettivene():
    url_base = "https://www.nettivene.com/en/purjevene?sortCol=enrolldate&ord=DESC&page={}"
    result = list()
    for i in range(1,get_n_pages()+1):
    # for i in range(1,2):
        url = url_base.format(str(i))
        print(url)
        r = requests.get(url)
        soup = BeautifulSoup(r.text, 'lxml')

        r1 = soup.find_all('a', class_ = 'childVifUrl tricky_link')
        r2 = soup.find_all('div', class_ = 'main_price')

        for b in r1:
            result.append([b.get_text(),b['href']])
            # print(b.get_text())
            # print(b['href'])
        l_res = len(result) - len(r2)
        for idx,b in enumerate(r2):
            # print(b.get_text())
            result[l_res+idx].append(b.get_text())
    # print(result)
    name = 'nettivene_boat_links_' + str(datetime.now().strftime("%Y.%m.%d_%H:%M:%S"))
    with open(os.getcwd() + '/boat_links/' + name + '.txt', 'w') as output:
        for boat in result:
            res = '|'.join(boat) + '\n'
            output.write(res)
    print("Boats total: " + str(len(result)))



if __name__ == "__main__":
    diff_parse_links()