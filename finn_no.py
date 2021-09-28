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


if __name__ == "__main__":
    eps.load_and_save('finn_no')
    pab.diff_parse_links('finn_no', 'd')

    # print(html)
    # html = pab.load_html_file('html/123_2021.03.06_13.07.43.html')
    # for i in extract_ads_finn_no(html):
    #     print(i)
    # pab.save_html_file("https://www.finn.no/boat/forsale/search.html?class=2188&page=1&sort=PUBLISHED_DESC", '123')
