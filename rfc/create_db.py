
def create_db():
    info_sailboatdata = "model length lwl description width draft_max draft_min weight keel_type ballast_weight steering_system hull_type first_built last_built builder designer linksailboatdata rigging_type sail_area ballast_type n_built mast_height id hull_material"
    info_nettivene = "header id_nettivene vehicle_brand vehicle_model price year_prod hull_material length width draft weight steering_system mast_height accessories note engine_information heating_information sail_information location coordinates link model_suggested model_id_suggested date_added date_deleted date_checked"
    basic_str = "ALTER TABLE boat_site_test01.nettivene ADD xxx varchar NULL;"



# basic_str = "xxx = db.Column(db.String())"

    for item in info_nettivene.split(" "):
        try:
            int(item)
        except Exception:
            print(basic_str.replace("xxx", item))


if __name__ == "__main__":
    create_db()



