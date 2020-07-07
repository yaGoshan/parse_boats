import requests
from datetime import datetime
from bs4 import BeautifulSoup
import os
import codecs
import string


def get_n_pages():
    url = "https://www.nettivene.com/en/purjevene"
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'lxml')
    n_page = int(soup.find("span", class_ = "totPage").text)
    return n_page

def parse_links():
    url_base = "https://www.nettivene.com/en/purjevene?sortCol=enrolldate&ord=DESC&page={}"
    result = list()
    # for i in range(1,get_n_pages()):
    for i in range(1,2):
        url = url_base.format(str(i))
        print(url)
        r = requests.get(url_base)
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
    print(result)
    name = 'nettivene_boats_' + str(datetime.now().strftime("%Y.%m.%d_%H:%M:%S"))
    with open(os.getcwd() + '/boat_links/' + name + '.html', 'w') as output:
        for boat in result:
            res = '|'.join(boat) + '\n'
            output.write(res)


def main():
    print("Hi!")
    return 0

if __name__ == "__main__":
    parse_links()