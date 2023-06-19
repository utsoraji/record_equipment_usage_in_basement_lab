import appconfig
from app.datastore.googleapi.credential import connect_gspread
from app.datastore.googleapi.spreadsheet_proxy import SpreadsheetProxy

gc = connect_gspread()


db = SpreadsheetProxy(gc, appconfig.MASTER_SPREADSHEET_KEY)

print(db.table_keys)

for key in db.table_keys:
    print(db[key].data())
