import psycopg2
import requests
from datetime import datetime
from bs4 import BeautifulSoup
import os
import codecs

def get_boat_number():
    url = "https://sailboatdata.com/sailboat"
    r = requests.get(url)
    boat_number = -1
    soup = BeautifulSoup(r.text, 'lxml')
    texts = soup.find_all('li')
    for text in texts:
        res = text.text.find('sailboats')
        if res != -1:
            boat_number = int(text.text[0:res])
            print("Boat number is:", boat_number)
    return boat_number


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

def load_and_save_html(link, name):
    url = link + "?units=metric"
    r = requests.get(url)

    html = r.text

    with open(os.getcwd() + '/html/' + name + ".html", "w") as output:
        output.write(html)