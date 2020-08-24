import json
import re
import time

from random import randint
from bs4 import BeautifulSoup
from selenium import webdriver


def writeJsonFile(data, fileName):
    with open("./good/" + fileName, 'a', encoding="UTF8") as outfile:
        json.dump(data, outfile, ensure_ascii=False)
        outfile.write(",")


def foo(name_find, driver):
    driver.find_element_by_id("searchboxinput").clear()
    time.sleep(2)

    # 군포시 + name_find 입력
    elem = driver.find_element_by_id("searchboxinput")
    elem.send_keys('군포시 ' + name_find)
    # 검색 클릭
    elem = driver.find_element_by_id("searchbox-searchbutton")
    elem.click()

    time.sleep(3)

    xy = driver.current_url
    x = xy.find('!3d')
    y = xy.find('!4d')
    longitude = xy[x + 3:y]
    latitude = xy[y + 3:]

    data = [longitude, latitude]

    return data


with open('good.json', 'rt', encoding='UTF8') as json_file:
    json_data = json.load(json_file)

    driver = webdriver.Chrome()
    driver.get("https://www.google.co.kr/maps")
    driver.implicitly_wait(3)

    count = 1

    for json_obj in json_data:

        if (count % 500 == 0):
            driver.close()

            driver = webdriver.Chrome()
            driver.get("https://www.google.co.kr/maps")
            driver.implicitly_wait(3)

        count += 1

        if (count % 100 == 0):
            print(f"{count} / {len(json_data)} 완료")

        try:
            random = randint(2, 4)
            time.sleep(random)

            data = foo(json_obj["REFINE_ROADNM_ADDR"], driver)

            new_json = {"SIGUN_NM": json_obj["SIGUN_NM"], "CMPNM_NM": json_obj["CMPNM_NM"], "INDUTYPE_NM": json_obj["INDUTYPE_NM"],
                        "REFINE_ROADNM_ADDR": json_obj["REFINE_ROADNM_ADDR"], "REFINE_LOTNO_ADDR": json_obj["REFINE_LOTNO_ADDR"],
                        "TELNO": json_obj["TELNO"], "REFINE_ZIPNO": json_obj["REFINE_ZIPNO"], "REFINE_WGS84_LAT": data[0], "REFINE_WGS84_LOGT": data[1],
                        "DATA_STD_DE": json_obj["DATA_STD_DE"], "URL": json_obj["URL"]}

            writeJsonFile(new_json, 'good.json')
        except:
            writeJsonFile(json_obj, 'bad.json')
