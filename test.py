import appconfig
from app.datastore.googleapi.credential import connect_gspread
from app.datastore.googleapi.spreadsheet_as_db import SpreadsheetAsDataBase

gc = connect_gspread()


db = SpreadsheetAsDataBase(gc, appconfig.MASTER_SPREADSHEET_KEY)

print(db.table_keys)

for key in db.table_keys:
    print(db[key].data())
