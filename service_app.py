import json
import time

import dbs
from dbs import Ad_nettivene
from dbs import db
import requests

def main():
    for boat in Ad_nettivene.query.all():
        if boat.location_osm == None:
            print(boat.header, boat.location)
            r = requests.get('https://api.opencagedata.com/geocode/v1/json?q='+boat.location+'&key=04fab3c1cf9f4ff3a6f04ed2c35c4991')
            print(r.json().get("status"))
            if r.json().get("status").get('code') == 200:
                data = r.json().get('results')[0]

                res = dict()
                res.update({"geometry": data.get("geometry")})
                res.update({"formatted": data.get("formatted")})
                res.update({"url": data.get("annotations").get("OSM").get("url")})
                boat.location_osm = str(res)
                db.session.commit()
                time.sleep(1)
                # input()
            else:
                print(r.json())
                input()
        else:
            print(boat.header, boat.location_osm)



if __name__ == "__main__":
    main()
