
def create_db():
    info = "1 model 2 length 3 lwl 4 description 5 width 6 draft_max 7 draft_min 8 weight 9 keel_type 10 ballast_weight 11 steering_system 12 hull_type 13 first_built 14 last_built 15 builder 16 designer 17 linksailboatdata 18 rigging_type 19 sail_area 20 ballast_type 21 n_built 22 mast_height 23 id 24 hull_material"
    # basic_str = "ALTER TABLE boat_site_test01.sailboat_models ADD xxx varchar NULL;"
    basic_str = "xxx = db.Column(db.String())"

    for item in info.split(" "):
        try:
            int(item)
        except Exception:
            print(basic_str.replace("xxx", item))


if __name__ == "__main__":
    create_db()