import psycopg2
import requests
from datetime import datetime
from bs4 import BeautifulSoup
import os
import codecs
import parse_ads_basics as pab

proxies = {
  'https': 'http://181.215.147.178:4787',
}




def get_file_name():
    boat_number = get_boat_number()
    file_name = os.getcwd() + r'/results/boat_pages_' + str(
        datetime.now().strftime("%Y.%m.%d_%H:%M:%S")) + "_" + str(boat_number) + ".txt"
    print(file_name)
    return file_name


def load_image_from_url(url, model):
    img_data = requests.get(url).content
    os.makedirs(os.getcwd() + r'/photo/' + model, exist_ok=True)
    pic_name = os.getcwd() + r'/photo/' + model+r'/' + url.split('/')[-1]
    with open(pic_name, 'wb') as handler:
        handler.write(img_data)


