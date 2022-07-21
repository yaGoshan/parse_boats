import os
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
import json

from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import SQLAlchemyError
import parse_ads_basics as pab
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://postgres:forget21@localhost/postgres"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)


class Ad_nettivene(db.Model):
    __tablename__ = "nettivene"
    __table_args__ = {"schema": "boat_site_test01"}
    header = db.Column(db.String())
    id_nettivene = db.Column(db.String(), primary_key=True, nullable=False)
    vehicle_brand = db.Column(db.String())
    vehicle_model = db.Column(db.String())
    price = db.Column(db.String())
    year_prod = db.Column(db.String())
    hull_material = db.Column(db.String())
    length = db.Column(db.String())
    width = db.Column(db.String())
    draft = db.Column(db.String())
    weight = db.Column(db.String())
    steering_system = db.Column(db.String())
    mast_height = db.Column(db.String())
    accessories = db.Column(db.String())
    note = db.Column(db.String())
    engine_information = db.Column(db.String())
    heating_information = db.Column(db.String())
    sail_information = db.Column(db.String())
    location = db.Column(db.String())
    coordinates = db.Column(db.String())
    link = db.Column(db.String())
    model_suggested = db.Column(db.String())
    model_id_suggested = db.Column(db.String())
    date_added = db.Column(db.String())
    date_deleted = db.Column(db.String())
    date_checked = db.Column(db.String())


def put_data_nettivene():
    list_of_ads = pab.get_files_list(os.getcwd()+"/boat_pages", "html", True)
    #
    for ad_path in list_of_ads:
        try:
            html = pab.load_text_file(ad_path)
            ad = extract_ad_nettivene(html)
            
            if Ad_nettivene.query.get(ad.id_nettivene) == None:
                db.session.add(ad)
                db.session.commit()
                print("Success! ", ad.header)
            else:
                print("Not Success!")
        except Exception as e:
            print("Not Success!", e, ad.header)
            db.session.rollback()
    # db.session.add()


def extract_ad_nettivene(html):
    ad = Ad_nettivene()
    soup = BeautifulSoup(html, 'lxml')
    # soup = BeautifulSoup(html, 'html.parser')

    ans = re.search('{"productInfo":(.*)}}', html)
    product_info = json.loads(ans.group(0)).get("productInfo")
    
    ad.id_nettivene = product_info.get("productID")
    ad.vehicle_brand = product_info.get("vehicleBrand")
    ad.vehicle_model = product_info.get("vehicleModel")
    ad.price = product_info.get("basePrice")
    ad.year_prod = product_info.get("vehicleYear")
    ad.location = product_info.get("locationRegion") + ", " + product_info.get("locationCity")
    ad.length = product_info.get("vehicleLength")

    ans = re.search('\{"products":(.*)}]}', html)
    ad.header = json.loads(ans.group(0)).get("products")[0].get('name')

    # print(soup.find_all("tr"))
    for item in soup.find_all('td'):
        if item.text == "Body material":
            ad.hull_material = item.findNext().text
        if item.text == "Steering system":
            ad.steering_system = item.findNext().text
        if item.text == "Length":
            ad.length = item.findNext().text
        if item.text == "Mast height":
            ad.mast_height = item.findNext().text
        if item.text == "Width":
            ad.width = item.findNext().text
        if item.text == "Weight":
            ad.weight = item.findNext().text
        if item.text == "Draught":
            ad.draft = item.findNext().text

    # print(ad.hull_material)
    # print(ad.steering_system)
    # print(ad.length)
    # print(ad.mast_height)
    # print(ad.weight)
    # print(ad.draft)
    accessories = str()
    sail_information = str()
    for item in soup.find_all('div', class_='acc_det'):
        if item.previous.text == 'Accessories':
            for item2 in item.find_all('div'):
                # print(item2.text)
                accessories += item2.text + "; "
            for item2 in item.fetchNextSiblings()[0].find_all('div'):
                # print(item2.text)
                accessories += item2.text + "; "
        # print(item.text)
        # if item.previous.text == 'Sail information':
        #     for item2 in item.find_all('div'):
        #         print(item2.text)
        #         sail_information += item2.text + "; "
    ad.accessories = accessories
    # ad.sail_information = sail_information
    # print(sail_information)

    note = str()
    for item in soup.find_all('p', class_="ma0"):
        note += item.text
    ad.note = note
    # print(ad.note)
    ad.date_added = str(datetime.now().strftime("%Y.%m.%d_%H.%M.%S"))

    return ad


if __name__ == "__main__":
    put_data_nettivene()