from dotenv import load_dotenv

load_dotenv()

import os

SERVICE_ACCOUNT_PATH = os.getenv("USAGEAPP_SERVICE_ACCOUNT_PATH")
MASTER_SPREADSHEET_KEY = os.getenv("USAGEAPP_MASTER_SPREADSHEET_KEY")
