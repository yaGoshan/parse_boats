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
import unidecode
import extract_parse_save as eps


# def parse_links_finn_no(print_=False):
#     """ Parses links to boat names, boat pages, prices(Norway krone) and year. """
#     site = 'finn_no'
#     url_base = "https://www.finn.no/boat/forsale/search.html?class=2188&page={}&sort=PUBLISHED_DESC"
#     result = list()
#     
#     try:
#         n_page = gnp.get_p_and_b(site)[0]
#         for i in range(1, n_page + 1):
#         # for i in range(1, 2):
#             url = url_base.format(str(i))
#             print('Current page: ', i, 'out of:', n_page)
#             r = pab.get_html_from_url(url)
#             boats = eps.extract_ads_finn_no(r)
#             if print_:
#                 for boat in boats:
#                     print(boat)
#             result += boats
#     finally:
#         name = 'finn_no_boat_links_' + str(datetime.now().strftime("%Y.%m.%d_%H.%M.%S"))
#         with open(os.getcwd() + '/finn_no_boat_links/' + name + '.csv', 'w') as csv_file:
#             writer = csv.writer(csv_file, delimiter=';')
#             for boat in result:
#                 writer.writerow(boat)
#         print("Boats total: " + str(len(result)))


if __name__ == "__main__":
    eps.load_and_save('finn_no')
    pab.diff_parse_links('finn_no', 'd')

    # print(html)
    # html = pab.load_html_file('html/123_2021.03.06_13.07.43.html')
    # for i in extract_ads_finn_no(html):
    #     print(i)
    # pab.save_html_file("https://www.finn.no/boat/forsale/search.html?class=2188&page=1&sort=PUBLISHED_DESC", '123')
