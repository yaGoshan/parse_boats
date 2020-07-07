import psycopg2
import requests
from datetime import datetime
import time
from bs4 import BeautifulSoup
import os
import codecs
import boat_parser_additional_functions as bp_add

def db_add_boat_link(link_info):
    conn = psycopg2.connect(dbname='postgres', user='postgres', password='postgres', host='localhost')
    cursor = conn.cursor()

    cursor.execute('INSERT INTO boat_list.list_of_links (link,model) VALUES (%s,%s);',
                   (link_info['link'], link_info['model']))
    conn.commit()
    cursor.close()
    conn.close()


""" If file name is None, then save boat links to DB and write info to file else, save links to file. """
def get_boat_pages_from_search(file_name=None, all_pages=False):
    i = 0
    page_total = int(bp_add.get_boat_number() / 100) + 1
    parse_delay = 0.1 # In seconds
    if all_pages == True:
        page_max = page_total
    else:
        page_max = 1

    url_base = "https://sailboatdata.com/sailboat?paginate=100&sort=name&page="

    """ Writing parse info ti file """
    if file_name == None:
        with open(bp_add.get_file_name(), 'a+') as output_file:
            output_file.write(
                "Parsing list: " + str(page_max) + '\n' + 'Pages total: ' + str(page_total) + '\nParse delay: ' + str(
                    parse_delay))
    """ Iterate over pages in search. """
    for n_page in range(1, page_max + 1):
        r = requests.get(url_base + str(n_page))
        time.sleep(parse_delay)
        print("Page: " + str(n_page))
        html = r.text
        soup = BeautifulSoup(html, 'lxml')

        """ Saving links to DB """
        if file_name == None:
            for boat_url in soup.find('tbody').find_all('a', href=True):
                db_add_boat_link({'link': boat_url.get('href'), 'model': boat_url.text})
        else:
            with open(file_name, 'a+') as output_file:
                i += 1
                print(i)
                for boat_url in soup.find('tbody').find_all('a', href=True):
                    output_file.write(boat_url.get('href') + "\n")

    with open(bp_add.get_file_name(), 'a+') as output_file:
        output_file.write("Parsing had been finished.")


def procced_list_of_links():
    parse_delay = 0.1
    conn = psycopg2.connect(dbname='postgres', user='postgres', password='postgres', host='localhost')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM boat_list.list_of_links')
    # cursor.execute("SELECT column_name FROM information_schema.columns where table_name='sailboat_models'")
    records = cursor.fetchall()

    conn.commit()
    cursor.close()
    conn.close()

    print('There is ' + str(len(records)) + ' boats.')
    i = 0
    for item in records:
        i = i + 1
        if i % 100 == 0:
            print('Proceeded ' + str(i))
        time.sleep(parse_delay)
        bp_add.load_and_save_html(item[0], item[1].replace('/','|'))