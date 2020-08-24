import json
import time
from random import randint

from bs4 import BeautifulSoup
from selenium import webdriver


def foo(name_find, driver):
    driver.find_element_by_name('q').clear()
    time.sleep(2)
    driver.find_element_by_name('q').send_keys('군포시 ' + name_find)

    element = driver.find_element_by_xpath('//*[@id="search.keyword.submit"]')
    driver.execute_script("arguments[0].click();", element)

    time.sleep(3)
    # info\.search\.place\.list
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')

    # 주소 지번주소 전화번호 url
    addr = soup.findAll("p", {"data-id": "address"})
    street_addr = soup.findAll("p", {"data-id": "otherAddr"})
    hp = soup.findAll("span", {"data-id": "phone"})
    url = soup.findAll("a", {"class": "moreview"})

    data = [addr[0]["title"], "경기 군포시 " + street_addr[0]["title"], hp[0].text, url[0]["href"]]

    # driver.close()
    return data


def makeFile(jsontxt, fileName):
    fileDirectory = "./makeFile/" + fileName
    f = open(fileDirectory, "a", encoding="UTF8")
    str1 = str(jsontxt)
    f.write(str1)
    f.write(",")
    f.close()


def writeJsonFile(data, fileName):
    with open("./makeFile/" + fileName, 'a', encoding="UTF8") as outfile:
        json.dump(data, outfile, ensure_ascii=False)
        outfile.write(",")


with open('data.json', 'rt', encoding='UTF8') as json_file:
    json_data = json.load(json_file)

    driver = webdriver.Chrome()
    driver.get("https://map.kakao.com/")
    driver.implicitly_wait(3)
    count = 0
    for json_obj in json_data:
        count += 1
        if (count % 100 == 0):
            print(f"{count} / {len(json_data)} 완료")
        # 랜덤으로 2~4초 쉬고
        try:
            random = randint(2, 4)
            time.sleep(random)

            try:
                data = foo(json_obj["CMPNM_NM"], driver)

                if (not ("군포시" in data[1])):
                    writeJsonFile(json_obj, "bad.json")
                    continue

                new_json = {"SIGUN_NM": "군포시", "CMPNM_NM": json_obj["CMPNM_NM"], "INDUTYPE_NM": json_obj["INDUTYPE_NM"],
                            "REFINE_ROADNM_ADDR": data[1], "REFINE_LOTNO_ADDR": data[0], "TELNO": data[2],
                            "REFINE_ZIPNO": json_obj["REFINE_ZIPNO"], "REFINE_WGS84_LAT": json_obj["REFINE_WGS84_LAT"],
                            "REFINE_WGS84_LOGT": json_obj["REFINE_WGS84_LOGT"], "DATA_STD_DE": json_obj["DATA_STD_DE"],
                            "URL": data[3]}

                writeJsonFile(new_json, "good.json")
                # makeFile(new_json, "good.json")
            except:
                # makeFile(json_obj, "bad.json")
                writeJsonFile(json_obj, "bad.json")
        except:
            print(json_obj)  # 오류나면 여기서 부터 다시 시작할끄야
            time.sleep(30)
