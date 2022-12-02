"""
This file handle json file
"""
import os
import json
import re


def get_int_ver(version: str):
    """
    vd: 2.1.560.99.33.22.11
    """

    str_splitted = version.split(".")
    str_concat = str_splitted[0] + str_splitted[1]

    if len(str_splitted[2]) > 3:
        third_part = str_splitted[2][:2]
    else:
        third_part = str_splitted[2]

    str_concat += third_part
    return int(str_concat)


def get_polaris_re(release: str):
    str_splitted = release.split(".")
    str_concat = str_splitted[0] + '.' + str_splitted[1][:1]
    return str_concat


def get_ise_re(release: str):
    str_concat = ''
    if len(release.split()) == 1:
        str_splitted = release.split('.')
        str_concat = str_splitted[0] + '.' + str_splitted[1]
    elif len(release.split()) == 3:
        string = release.split()
        str_splitted = string[0]
        str_concat = str_splitted.split(".")
        str_concat = str_concat[0] + '.' + str_concat[1]
    return str_concat


# print(get_ise_re('2.7.0.356 patch: 8'))

def collect_file():
    """This func use to collect meta.json file into 1 list"""
    data = []
    path_to_json = '/home/administrator/Documents/challenges/metajson-20221014T095050Z-001/metajson/'
    for file_name in [file for file in os.listdir(path_to_json) if file.endswith('.json')]:
        with open(path_to_json + file_name, encoding='utf8') as json_file:
            json_item = json.load(json_file)
            data.append(json_item)
    return data


def mapping_dnac(item):
    """This func process corresponding release and version"""
    res = {}
    int_version = get_int_ver(item["dna_packages_version"]["sd-access"])
    # if int_version == 21388 or int_version == 21389 or int_version == 21390 or int_version == 21391:
    if int_version < 21400 and int_version >= 21300:
        res["dnac_release"] = 'Shockwave'
    elif int_version >= 21460 and int_version < 21510:
        res["dnac_release"] = 'Fury'
    elif int_version >= 21510 and int_version < 21560:
        res["dnac_release"] = 'Guardian'
    elif int_version >= 21560 and int_version < 21610:
        res["dnac_release"] = 'Groot'
    elif int_version >= 21610 and int_version < 21660:
        res["dnac_release"] = 'Ghost'
    elif int_version >= 21660:
        res["dnac_release"] = 'Halleck'

    res["dnac_version"] = (item["dna_packages_version"]["sd-access"])
    return res


def mapping_ise(item):
    if 'ise_version' not in item:
        res = {
        'ise_release': "",
        'ise_version': ""
    }
        return res
    ise_release = get_ise_re(item['ise_version'])
    res = {
        'ise_release': ise_release,
        'ise_version': item['ise_version']
    }
    return res


Model = [['CAT4k', 'Catalyst38xx', 'CAT6k', 'N7k', '9200', '9300',
          '9500', 'C94', 'C96'], ['ISR', 'ASR', '1001-HX', '4451-X'], ['9800', '5520', '5504', '8540', '3504'],
         ['CDB', 'IE-3', 'IE-44', 'IE-5', "IE-", "3560CX"], ['AIR', 'AXE', 'AXI', 'I', 'C91', '4800', '3800', '1800S', '2800', '3700E']]

Special_model = [['38'], [], [], ['35'], []]
Product = {'Switch': [], 'Router': [],
           'Controllers': [], 'IoT': [], "Access Point": []}
type_Product = ['Switch', 'Router', 'Controllers', 'IoT', "Access Point"]


def check_platform(platform):
    if platform[0:4] == "AIR-":
        test_two = platform[6:10]
        for index, models in enumerate(Model):
            for model in models:
                if model in test_two:
                    return type_Product[index]
        return type_Product[4]
    elif platform[0:4] == "WS-C":
        test_one = platform[4:6]
        for index, models in enumerate(Special_model):
            for model in models:
                if model in test_one:
                    return type_Product[index]
    else:
        for index, models in enumerate(Model):
            for model in models:
                if model in platform:
                    return type_Product[index]


def check_type(type):
    type_split = type.split(" ")
    model_type = None
    for i in type_split:
        if not re.match("^[A-Za-z\-]*$", i):
            model_type = i

    for index, models in enumerate(Model):
        for model in models:
            if (model in model_type) or (model in ("C" + model_type)):
                return type_Product[index], model_type


def classify(product, model):
    for key, value in Product.items():
        if product == key and model not in Product[key]:
            Product[key].append(model)
    return Product


def check(data_json):

    meta = []
    device_version = data_json["device_version"]
    for j in device_version:
        platform = j["platform"]
        type = j["type"]
        if check_platform(platform):
            type_pro, model = check_type(type)
            if check_platform(platform) == type_pro:
                classify(type_pro, model)

                meta.append({
                    f"{type_pro}": model,
                })
            else:
                classify(check_platform(platform), model)

                meta.append({
                    f"{check_platform(platform)}": model,
                })

    return meta, Product


def mapping_polaris(item):
    """This func process corresponding polaris release and version"""
    b = []
    for a in item['device_version']:
        release = get_polaris_re(a['version'])
        res = {
            'version': a["version"],
            'release': release
        }
        b.append(res)
    return b
