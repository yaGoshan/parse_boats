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


def save_boats_pages():
    with open(pab.get_path() + 'saildata_boat_links/info_2020.09.08_00:14:35.csv', 'r') as file:
        for x in file:
            name = x.split(';')[1].split('/')[-1]
            link = x.split(';')[1][:-1]
            pab.save_html_file(link, name)
            print(name, link)


if __name__ == '__main__':
    save_boats_pages()
