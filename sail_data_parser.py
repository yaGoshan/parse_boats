import psycopg2
import requests
from datetime import datetime
import time
from bs4 import BeautifulSoup
import os
import codecs
import boat_parser_additional_functions as bp_add
import parse_boat_links as bl
"""
    Data to extract:
Model:        
Length(Length max):
LWL(Length waterline:
Beam(width):
Mast height:
Draft (max, draught):
Draft (min):
Keel type: 
Weight
Ballast:
Steering system:
Hull material:
Class:
Ballast Type:
Hull shape:(mono or multi)

Hull Type:
Rigging Type:


First Built:
Last Built:
Builder:
Designer:

Private:
Fuel
Location
Registration
Engine
Sails
Power
Accessories
Heating
Cooking Type: Gas, Alcohol; Oven?
Toilet
Note
Autopilot
Tanks (Fuel and Water)

"""

"""
manufacturer, model, length, LWL, description, width, id, Draft(max), Draft(min),
weight, keel_type, ballast_weight, steering_system, hull_type, first_built,
last_built, builder, designer, linksailboatdata, rigging_type, sail_area, ballast_type,
n_built,mast_height,hull_material

{'Hull Type': 'Fin with rudder on skeg', 'Rigging Type': 'Masthead Sloop', 'LOA': '7.90', 'LWL': '6.10', 
'Be': '2.67', 'S.A. (reported)': '24.25', 'Draft (max)': '1.40', 'Draft (min)': '', 'Displacement': '1905', 
'Ballast': '750', 'Construction': 'FG', 'Ballast Type': 'Lead', 
'Make': 'Volvo Penta', 'Model': 'MD5', 'Type': 'Diesel', 'HP': '10', 
'I': '9.38', 'J': '3.10', 'P': '8.12', 'E': '2.39', 'SPL/TPS': '', 'ISP': '', 
'S.A. Fore': '14.54', 'S.A. Main': '9.69', 'S.A./Disp. (calc.)': '16.07', 'Est. Forestay Len.': '9.88', 'model': 'ALBIN 79'}

"""


def db_add_boat_model(boat_info, id):
    conn = psycopg2.connect(dbname='postgres', user='postgres', password='postgres', host='localhost')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO boat_list.sailboat_models (model,length, hull_material, lwl, width, draft_max,'
                   'draft_min, weight, ballast_weight, keel_type,first_built, last_built, n_built,'
                   ' rigging_type, ballast_type, linksailboatdata, id) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,'
                   '%s,%s,%s,%s,%s,%s,%s,%s,%s);',
                   (boat_info.get('model'),boat_info.get('LOA'),boat_info.get('Construction'),boat_info.get('LWL'),boat_info.get('Beam')
                    ,boat_info.get('Draft (max)'),boat_info.get('Draft (min)'),boat_info.get('Displacement')
                    ,boat_info.get('Ballast'),boat_info.get('Hull Type'),boat_info.get('First Built')
                    ,boat_info.get('Last Built'),boat_info.get('# Built'),boat_info.get('Rigging Type')
                    ,boat_info.get('Ballast Type') ,boat_info.get('link'),id))
    conn.commit()
    cursor.close()
    conn.close()




def db_connect():
    conn = psycopg2.connect(dbname='postgres', user='postgres', password='postgres', host='localhost')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM boat_list.sailboat_models')
    # cursor.execute("SELECT column_name FROM information_schema.columns where table_name='sailboat_models'")
    records = cursor.fetchall()
    print(records)
    for item in records:
        print(item)
    conn.commit()
    cursor.close()
    conn.close()





def get_sail_data_from_html(html):
    soup = BeautifulSoup(html, 'lxml')

    boat_model = soup.find_all("h1")[1].text.replace(' ','_')
    """ Load photos """
    pics = soup.find_all("img",{"class":"img-responsive center-block"})
    # for pic in pics:
    #     # print(pic['src'])
    #     bp_add.load_image_from_url(pic['src'], boat_model)

    """ Get data """
    desc = soup.find_all("div", class_ = "col-sm-3")
    desc = desc + soup.find_all("div", class_ = "col-sm-2")
    # print(desc)
    a = []
    for item in desc:
        obj = item.text.strip()
        if obj[-1:] == ':': obj = obj[:-1]
        if obj[-2:] == ' m': obj = obj[:-2]
        if obj[-2:] == 'kg': obj = obj[:-3]
        if obj[-2:] == 'm2': obj = obj[:-3]
        if obj[-4:-3] == ',': obj = obj.replace(',','')
        if obj.find(',') == True: obj = obj.replace(',','')

        a.append(obj)
    b = dict(zip(a[::2], a[1::2]))
    b.update({"model":boat_model.replace('_',' ')})
    link = soup.find('a',class_ = 'btn-default').get('href')
    b.update({'link':link})

    for key in b.keys():
        if b.get(key) == '':
            b.update({key:'-1'})

    return b

def proceed_loaded_htmls():
    list_of_boat_files =  os.listdir(os.getcwd()+'/html')
    # i = 4079
    for i in range(0,len(list_of_boat_files)):

        if i % 20 == 0:
            print('Proceeded ' + str(i))
        # time.sleep(0.1)

        html = codecs.open(os.getcwd()+'/html/' + list_of_boat_files[i], "r")
        boat_info = get_sail_data_from_html(html)
        db_add_boat_model(boat_info, i)
        i = i + 1



# def main():
    """ Parse links to boat pages, to list_of_links BD """
    # bl.get_boat_pages_from_search(all_pages=True)
    """ Get links from DB table 'list_of_links', and load and save html files """
    # procced_list_of_links()

    """ Proceed data from html files. Contains get_sail_data_from_html, save_pics and add info to DB """
    # proceed_loaded_htmls()


def main():

    conn = psycopg2.connect(dbname='postgres', user='postgres', password='postgres', host='localhost')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM boat_list.sailboat_models')
    # cursor.execute("SELECT column_name FROM information_schema.columns where table_name='sailboat_models'")
    records = cursor.fetchall()[:20]

    print(type(records))
    for i in range(len(records)):
        buf = list(records[i])
        buf[1] = buf[1].replace(' ', '_')
        records[i] = tuple(buf)
        print(records[i] )

    print(records[0])
    print(type(records[0]))
    conn.commit()
    cursor.close()
    conn.close()

    return records





if __name__ == "__main__":
    main()
