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
    location_osm = db.Column(db.String())
    link = db.Column(db.String())
    model_suggested = db.Column(db.String())
    model_id_suggested = db.Column(db.String())
    date_added = db.Column(db.String())
    date_deleted = db.Column(db.String())
    date_checked = db.Column(db.String())