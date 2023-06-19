from app.datastore.googleapi.g_master_provider import GoogleMasterProvider
from app.model.equipment import Equipment
from scraping.fetch_equipments import fetch_equipments, open_driver

with open_driver() as driver:
    fetched_equipments = fetch_equipments(driver)

print(fetched_equipments)
# current_equipments = GoogleMasterProvider().equipments


# for f in fetched_equipments:
#     if f.name_kanakanji in current_equipments.keys():
#         current_equipments[f.name_kanakanji] = f

# print(current_equipments)
