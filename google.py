import json
import re
import time

from random import randint
from bs4 import BeautifulSoup
from selenium import webdriver

def valid_Inner(string):
    regex = re.compile(r'\d{3,4}-\d{3,4}-\d{4}')

    if (regex.search(string)):
        return string
    else:
        return ''

def writeJsonFile(data, fileName):
    with open("./makeFile/bad/" + fileName, 'a', encoding="UTF8") as outfile:
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

    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')

    addr = soup.findAll("div", {"class": "ugiz4pqJLAG__primary-text gm2-body-2"})

    if not len(addr):
        elem = driver.find_element_by_class_name("section-result:first-child")
        elem.click()

        time.sleep(3)

        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')
        addr = soup.findAll("div", {"class": "ugiz4pqJLAG__primary-text gm2-body-2"})

    address = addr[0].text.replace("KR", "")  # 주소
    hp = valid_Inner(addr[2].text)  # hp

    xy = driver.current_url
    x = xy.find('!3d')
    y = xy.find('!4d')
    longitude = xy[x + 3:y]
    latitude = xy[y + 3:]

    data = [address, hp, longitude, latitude]

    return data


with open('makeFile/bad.json', 'rt', encoding='UTF8') as json_file:
    json_data = json.load(json_file)

    driver = webdriver.Chrome()
    driver.get("https://www.google.co.kr/maps")
    driver.implicitly_wait(3)

    count = 1

    for json_obj in json_data:

        if(count%500 == 0):
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

            data = foo(json_obj["CMPNM_NM"], driver)

            if (not ("군포시" in data[0])):
                writeJsonFile(json_obj, "bad.json")
                continue

            address = "경기도 군포시"+ data[0].replace("경기도", "").replace("군포시", "").replace("  ", " ")

            new_json = {"SIGUN_NM": "군포시", "CMPNM_NM": json_obj["CMPNM_NM"], "INDUTYPE_NM": json_obj["INDUTYPE_NM"],
                        "REFINE_ROADNM_ADDR": json_obj["REFINE_ROADNM_ADDR"], "REFINE_LOTNO_ADDR": address,
                        "TELNO": data[1], "REFINE_ZIPNO": json_obj["REFINE_ZIPNO"], "REFINE_WGS84_LAT": data[3],
                        "REFINE_WGS84_LOGT": data[2], "DATA_STD_DE": json_obj["DATA_STD_DE"]}

            writeJsonFile(new_json, 'good.json')
        except:
            writeJsonFile(json_obj, 'bad.json')
