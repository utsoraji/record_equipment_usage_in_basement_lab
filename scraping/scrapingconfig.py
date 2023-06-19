from dotenv import load_dotenv

load_dotenv()

import os

PROFILE_DIR = os.getenv("SCRAPING_PROFILE_DIR")
ACCOUNT_NAME = os.getenv("SCRAPING_ACCOUNT_NAME")
EQUIPMENTS_URL = os.getenv("SCRAPING_EQUIPMENTS_URL")
