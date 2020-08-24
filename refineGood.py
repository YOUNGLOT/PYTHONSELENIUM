import json
import time
from random import randint

from bs4 import BeautifulSoup
from selenium import webdriver

with open('makeFile/good.json', 'rt', encoding='UTF8') as json_file:
    json_data = json.load(json_file)

    driver = webdriver.Chrome()
    driver.get("https://map.kakao.com/")
    driver.implicitly_wait(3)

    for json_obj in json_data:

        data = json_obj["REFINE_LOTNO_ADDR"]
        datas = data.split(" ")
        print("여긴데")
        print(datas[1])

