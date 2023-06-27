import hashlib
import time
from dataclasses import dataclass

import requests
from selenium import webdriver
from selenium.common import WebDriverException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

import scraping.scrapingconfig as config


def open_driver():
    options = Options()
    options.add_argument("--user-data-dir=" + config.PROFILE_DIR)
    options.add_argument(f"--profile-directory={config.ACCOUNT_NAME}")
    options.add_argument("--disable-dev-shm-usage")
    return webdriver.Chrome(
        service=ChromeService(ChromeDriverManager().install()), options=options
    )


@dataclass(frozen=True)
class FetchedEquipment:
    name_kanakanji: str
    image_url: str
    location: str


def wait_for_element(driver, by: By, value):
    count = 0
    while True:
        try:
            time.sleep(1)
            return driver.find_element(by=by, value=value)
        except:
            count += 1
            if count > 10:
                raise "Timeout"
            pass


def fetch_equipments(driver):
    driver.get(config.EQUIPMENTS_URL)

    wait_for_element(driver, By.TAG_NAME, "h1")

    ret: list[FetchedEquipment] = []

    sections = driver.find_elements(by=By.TAG_NAME, value="section")
    room = None
    for i in range(1, len(sections) + 1):
        try:
            room = driver.find_element(
                by=By.XPATH,
                value=f"//section[{i}]/div[2]/div/div/div/div/div/div/div/div/h2",
            )
            print(f"Room: {room.text}")
        except WebDriverException:
            pass

        if room:
            equipments = driver.find_elements(
                by=By.XPATH, value=f"//section[{i}]/div[2]/div/div"
            )
            # print(len(equipments))
            for j in range(1, len(equipments) + 1):
                imgsrc = None
                try:
                    img = driver.find_element(
                        by=By.XPATH,
                        value=f"//section[{i}]/div[2]/div/div[{j}]/div/div/div[1]/div/div/div/div/img",
                    )
                    imgsrc = img.get_attribute("src")
                    hash = hashlib.md5(requests.get(imgsrc).content).hexdigest()

                    # print(f"Image: {imgsrc}")
                except WebDriverException:
                    pass
                h3s = driver.find_elements(
                    by=By.XPATH,
                    value=f"//section[{i}]/div[2]/div/div[{j}]/div/div/div[2]/div/div/div/h3",
                )
                name = "".join([h3.text for h3 in h3s])
                if name:
                    print(f"Name: {name}")
                    ret.append(FetchedEquipment(name, imgsrc, room.text))

    return ret


# /html/body/div[1]/div/div[2]/div[3]/div/div[1]/section[5]/div[2]/div/div[1]/div/div
# //*[@id="h.5f7abb62f0f94365_3"]/div/div/div/img
# /html/body/div[1]/div/div[2]/div[3]/div/div[1]/section[5]/div[2]/div/div[1]/div/div/div[1]/div/div/div/div/img
# /html/body/div[1]/div/div[2]/div[3]/div/div[1]/section[5]/div[2]/div/div[1]/div/div/div[2]/div/div/div/h3[1]
# /html/body/div[1]/div/div[2]/div[3]/div/div[1]/section[8]/div[2]/div/div[2]
