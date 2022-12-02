import pymongo
from pymongo.database import Database
from pymongo import MongoClient
from selenium import webdriver
from selenium.webdriver.edge.service import Service as EdgeService
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.wait import WebDriverWait
import datetime
import logging
import config
import constanst_var as var
from helper import mapping_dnac, check, mapping_ise, mapping_polaris
import time
import bson
import json
import os
import utils



class data_processing:

    def connect_db(self):
        try:
            self.root = utils.Collect_connection().connect_collect_new_dashboard()
            self.record = utils.Collect_connection().connect_collect_record()
            self.inventory = utils.Collect_connection().connect_collect_record_inventory()
            self.record.create_index([('dnac_release', pymongo.ASCENDING), ('dnac_version', pymongo.ASCENDING), 
                                ('polaris_release', pymongo.ASCENDING), ('polaris_version', pymongo.ASCENDING),  
                                ('ise_release', pymongo.ASCENDING),('ise_version', pymongo.ASCENDING)], unique = True)
            self.inventory.create_index([('dnac_release', pymongo.ASCENDING), ('dnac_version', pymongo.ASCENDING),  
                                ('polaris_release', pymongo.ASCENDING), ('polaris_version', pymongo.ASCENDING), 
                                    ('Switch', pymongo.ASCENDING), ('Router', pymongo.ASCENDING), ('Access Point', pymongo.ASCENDING), 
                                    ('IoT', pymongo.ASCENDING), ('Controllers', pymongo.ASCENDING)], unique = True)
        except Exception as e:
            return e
    def action(self, mode):
        root = self.root
        inventory = self.inventory
        record = self.record
        try:
            new_list = []
            path_to_json = f'meta/{mode}/'
            for file_name in [file for file in os.listdir(path_to_json) if file.endswith('.json')]:
                with open(path_to_json + file_name, encoding='utf8') as json_file:
                    json_item = json.load(json_file)
                    new_list.append(json_item)

            for item in new_list:
                all = []
                all.append(item)
                dnac_list = list(map(mapping_dnac, all))
                polaris_list = list(map(mapping_polaris, all))
                ise_list = list(map(mapping_ise, all))
                product_list, Product = check(item)

                if config.Product == {}:
                    config.Product = Product
                else:
                    for key, value in Product.items():
                        if Product[key] != config.Product[key]:
                            total = list(set(Product[key] + config.Product[key]))
                            config.Product[key] = total

                inventory_list = {
                    'dnac_release' : dnac_list[0]['dnac_release'],
                    'dnac_version' : dnac_list[0]['dnac_version'],
                }

                dnac = {

                    'dnac_release' : dnac_list[0]['dnac_release'],
                    'dnac_version' : dnac_list[0]['dnac_version'],
                    'aireos_release': None,
                    'aireos_version': None
                }
                ise = {
                    'ise_release' : ise_list[0]['ise_release'],
                    'ise_version' : ise_list[0]['ise_version']
                }
                dnac.update(ise)

                for index,polaris in enumerate(polaris_list[0]):
                    compatible = {}
                    inventory_item = {}
                    
                    res = {
                        'polaris_release' : polaris['release'],
                        'polaris_version' : polaris['version'],

                    }
                    compatible.update(dnac)
                    compatible.update(res)
                    compatible.update({"_id": bson.ObjectId()})

                    res.update(product_list[index])

                    inventory_item.update(inventory_list)
                    inventory_item.update(res)
                    inventory_item.update({"_id": bson.ObjectId()})

          
                    try:
                        record.insert_one(compatible)
                    except:
                        continue
                    try:
                        inventory.insert_one(inventory_item)
                    except:
                        continue
        except Exception as e:
            return e

    def save_product(self):
        with open('constanst_var.py', 'w') as f:
            f.write('PRODUCT = ')
            json.dump(config.Product , f, indent=4)
            f.close()




