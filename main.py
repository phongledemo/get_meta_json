from pymongo.database import Database
from pymongo import MongoClient
import pymongo
from selenium import webdriver
from selenium.webdriver.edge.service import Service as EdgeService
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.wait import WebDriverWait
from config import username, userInput_id, passwordInput_id, password, DNAC_Shockwave_Solution, metajson_xpath, login_button_id,\
    trust_browser_button_id, tbody_xpath, information_metajson_xpath, DNAC_Guardian_Solution, log, try_again_loading, database
import logging
from logging import config
import time
import json, os


log_config = log
config.dictConfig(log_config)
logger = logging.getLogger("root")

def connect_and_savejson(mode:str , try_connect):
    try:
        client = MongoClient(database)
        db : Database = client.get_database("dashboard")
        conn = db.get_collection("root_new")
    except:
        if try_connect == 0:
            logger.error("Can not connect to database")
            return "Can not connect to database"
        connect_and_savejson(mode, try_connect - 1)
    path_to_json = f'meta/{mode}/'
    for file_name in [file for file in os.listdir(path_to_json) if file.endswith('.json')]:
        with open(path_to_json + file_name, encoding='utf8') as json_file:
            json_item = json.load(json_file)
            if conn.find_one({"url":json_item["url"]}):
                continue
            conn.insert_one(json_item)

def check_exists_byOptions(drivers, option: str, infor: str, try_again: int) -> bool:
    try:
        if option == "ID":
            drivers.find_element(By.ID, infor)
        elif option == "NAME":
            drivers.find_element(By.NAME, infor)
        elif option == "CSS_SELECTOR":
            drivers.find_element(By.CSS_SELECTOR, infor)
        elif option == "CLASS_NAME":
            drivers.find_element(By.CLASS_NAME, infor)
        elif option == "TAG_NAME":
            drivers.find_element(By.TAG_NAME, infor)
        elif option == "XPATH":
            drivers.find_element(By.XPATH, infor)
    except NoSuchElementException as e:
        if try_again == 0:
            logger.error(e)
            return False
        check_exists_byOptions(drivers, option, infor, try_again - 1)
    return True


def Login_and_Authenticate(driver, try_again: int) -> bool:
    try:
        driver.find_element(By.ID, userInput_id).send_keys(username)
        driver.find_element(By.ID, login_button_id).click()
        WebDriverWait(driver, 60).until(
            EC.visibility_of_all_elements_located(
                (By.ID, passwordInput_id))
        )
        driver.find_element(
            By.ID, passwordInput_id).send_keys(password)
        driver.find_element(By.ID, login_button_id).click()
        WebDriverWait(driver, 60).until(
            EC.visibility_of_all_elements_located(
                (By.ID, trust_browser_button_id))
        )
        driver.find_element(By.ID, trust_browser_button_id).click()
        WebDriverWait(driver, 60).until(
            EC.visibility_of_all_elements_located(
                (By.XPATH, tbody_xpath))
        )
    except Exception as e:
        if try_again == 0:
            logger.error(e)
            return False
        Login_and_Authenticate(driver, try_again - 1)
    return True


def DNAC(driver, mode: str, try_again: int):
    if mode == "shockwave":
        driver.get(DNAC_Shockwave_Solution)
    elif mode == "guardian":
        driver.get(DNAC_Guardian_Solution)
    else:
        logger.error("No found mode")
        return False
    try:
        link_href = []
        if not Login_and_Authenticate(driver, try_again=try_again_loading):
            return "Error"
        if not check_exists_byOptions(driver, "XPATH", tbody_xpath, try_again=try_again_loading):
            return "Error"
        tbody = driver.find_element(
            By.XPATH, tbody_xpath)

        a_tags = tbody.find_elements(By.TAG_NAME, 'a')

        for i in a_tags:
            try:
                if "earms-trade.cisco.com" in i.get_attribute("href"):
                    link_href.append(i.get_attribute("href"))
            except Exception as e:
                return e
        return link_href
    except Exception as e:
        if try_again == 0:
            logger.error(e)
            return e
        DNAC(driver, mode, try_again - 1)


def download_metajson(link_href: list, mode: str, try_again) -> bool|list:
    correct_link = []
    if not link_href:
        if try_again == 0:
            return False
        download_metajson(link_href, mode, try_again - 1)
    for index, value in enumerate(link_href):
        driver.get(value)
        try:
            element = WebDriverWait(driver, 30).until(
                EC.presence_of_element_located(
                    (By.XPATH, metajson_xpath))
            )
            element.click()
            element = WebDriverWait(driver, 30).until(
                EC.visibility_of_all_elements_located(
                    (By.XPATH, information_metajson_xpath))
            )
            time.sleep(4)
            text = driver.find_element(
                By.XPATH, information_metajson_xpath).text
            text = dict(eval(text))
            text.update({"url":link_href[index]})
            with open('./meta/' + mode + f'/meta ({index}).json', 'w') as outfile:
                json.dump(text, outfile, indent=4, separators=(", ", ": "))
                correct_link.append(link_href[index])
        except:
            pass
    return correct_link


def run(driver, mode: str, try_again):
    try:
        link_herf = DNAC(driver, mode, try_again=try_again_loading)
        correct_link = download_metajson(link_herf, mode, try_again=try_again_loading)
        return correct_link
    except:
        if try_again == 0:
            logger.error("Error")
            return False
        run(driver, mode, try_again - 1)


if __name__ == "__main__":
    driver = webdriver.Edge(service=EdgeService(
        EdgeChromiumDriverManager().install()))
    modes = ["shockwave", "guardian"]
    for mode in modes:
        run(driver, mode, try_again=try_again_loading)
        connect_and_savejson(mode=mode, try_connect=try_again_loading)