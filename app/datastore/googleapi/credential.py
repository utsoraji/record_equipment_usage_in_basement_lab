import gspread
from google.oauth2 import service_account

import appconfig


def connect_gspread() -> gspread.Client:
    return gspread.service_account(filename=appconfig.SERVICE_ACCOUNT_PATH)


def get_credentials(scopes: list[str]) -> service_account.Credentials:
    return service_account.Credentials.from_service_account_file(
        appconfig.SERVICE_ACCOUNT_PATH,
        scopes,
    )
