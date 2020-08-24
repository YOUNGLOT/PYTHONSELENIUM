import json
"""
def writeJsonFile(data, fileName):
    with open("./" + fileName, 'a', encoding="UTF8") as outfile:
        json.dump(data, outfile, ensure_ascii=False)
        outfile.write(",")

with open('good.json', 'rt', encoding='UTF8') as json_file:
    json_data = json.load(json_file)

    for json_obj in json_data:

        if(json_obj["REFINE_WGS84_LAT"].replace(".","").isdigit()):
            writeJsonFile(json_obj, 'foo.json')
"""
with open('foo.json', 'rt', encoding='UTF8') as json_file:
    json_data = json.load(json_file)
    print(len(json_data))


