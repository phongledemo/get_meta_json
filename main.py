from pymongo.database import Database
from pymongo import MongoClient
import pymongo
from selenium import webdriver
from selenium.webdriver.edge.service import Service as EdgeService
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.wait import WebDriverWait
from data_process import data_processing
from config import username, userInput_id, passwordInput_id, password, DNAC_Shockwave_Solution, metajson_xpath, login_button_id,\
                trust_browser_button_id, tbody_xpath_1, tbody_xpath_2, information_metajson_xpath, DNAC_Guardian_Solution, DNAC_Ghost_Solution, \
                DNAC_Groot_Solution, log, try_again_loading, database, big_table, Wiki_Cisco_Page
import logging
from logging import config
import time
import json, os
import datetime
from functools import wraps
import sys


log_config = log
log_config['handlers']['file']['filename'] = 'log/'+f'{((str(datetime.datetime.now()).split(".")[0]).replace(":","-")).replace(" ","_")}.log'
config.dictConfig(log_config)
logger = logging.getLogger("root")
global_logger = logger

def graceful_exit():
    sys.exit()

def debug_decorator(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        func_name = func.__name__
        try:
            if type(args[0]) == list and len(args[0]) > 20:
                logger.debug(f'Entering function : {func_name} with args: list with len {len(args[0])} and {tuple(list(args)[1:])} kwargs {kwargs}')
            else:
                logger.debug(f'Entering function : {func_name} with args {args} kwargs {kwargs}')
        except:
            logger.debug(f'Entering function : {func_name} with args {args} kwargs {kwargs}')
        ret_string = func(*args, **kwargs)
        logger.debug(f'Leaving function : {func_name}')
        return ret_string
    return wrapper


@debug_decorator
def connect_and_savejson(mode:str , try_connect):
    try:
        client = MongoClient(database)
        db : Database = client.get_database("dashboard")
        conn = db.get_collection("root_new")
        logger.info(f"Connect to db successfully")
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

@debug_decorator
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
        logger.info(f"{option} {infor} exists")
    except NoSuchElementException as e:
        if try_again == 0:
            logger.error(e)
            return False
        check_exists_byOptions(drivers, option, infor, try_again - 1)
    return True

@debug_decorator
def Login_and_Authenticate(driver) -> bool:
    try:
        WebDriverWait(driver, 60).until(
            EC.visibility_of_all_elements_located(
                (By.ID, userInput_id))
        )
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
                (By.XPATH, big_table))
        )
        logger.info("Login successfully")
    except Exception as e:
        logger.error("Login fail")
        logger.error(e)
        return False
    return True


@debug_decorator
def DNAC(driver, mode: str, try_again: int):

    tbody_xpath = tbody_xpath_2

    if mode == "shockwave":
        driver.get(DNAC_Shockwave_Solution)
    elif mode == "guardian":
        driver.get(DNAC_Guardian_Solution)
    elif mode == "groot":
        driver.get(DNAC_Groot_Solution)
        tbody_xpath = tbody_xpath_1
    elif mode == "ghost":
        driver.get(DNAC_Ghost_Solution)
    else:
        logger.error("No found mode")
        return False
    try:
        link_href = []
        if not check_exists_byOptions(driver, option = "XPATH", infor = tbody_xpath, try_again=try_again_loading):
            return False
        tbody = driver.find_element(
            By.XPATH, tbody_xpath)

        a_tags = tbody.find_elements(By.TAG_NAME, 'a')

        for i in a_tags:
            try:
                if "earms-trade.cisco.com" in str(i.get_attribute("href")):
                    link_href.append(i.get_attribute("href"))
            except Exception as e:
                return e
        return link_href

    except Exception as e:
        if try_again == 0:
            logger.error(e)
            return e
        DNAC(driver, mode, try_again - 1)

@debug_decorator
def download_metajson(link_href: list, mode: str, try_again) -> bool|list:
    correct_link = []
    count = 0
    len_link_href = len(link_href)
    if not link_href:
        if try_again == 0:
            return False
        download_metajson(link_href, mode, try_again - 1)
    for index, value in enumerate(link_href):
        driver.get(value)
        try:
            element = WebDriverWait(driver, 20).until(
                EC.presence_of_element_located(
                    (By.XPATH, metajson_xpath))
            )
            element.click()
            element = WebDriverWait(driver, 20).until(
                EC.visibility_of_all_elements_located(
                    (By.XPATH, information_metajson_xpath))
            )
            time.sleep(1.5)
            text = driver.find_element(
                By.XPATH, information_metajson_xpath).text
            text = dict(eval(text))
            text.update({"url":link_href[index]})
            count += 1
            with open('./meta/' + mode + f'/meta ({index}).json', 'w') as outfile:
                json.dump(text, outfile, indent=4, separators=(", ", ": "))
                correct_link.append(link_href[index])
        except:
            pass
    logger.info(f"Download meta.json rate: ({count} links)/({len_link_href} links) from {mode} cisco page to local successful")
    return correct_link

@debug_decorator
def run(driver, mode: str):
    try:
        link_herf = DNAC(driver, mode, try_again=try_again_loading)
        correct_link = download_metajson(link_herf, mode, try_again=try_again_loading)
        return correct_link
    except:
        logger.error("Function run fail")
        return False


if __name__ == "__main__":
    driver = webdriver.Edge(service=EdgeService(
        EdgeChromiumDriverManager().install()))

    driver.get(Wiki_Cisco_Page)
    if not Login_and_Authenticate(driver):
        graceful_exit()
    modes = ["guardian", "shockwave", "groot", "ghost"]

    shrt = data_processing(logger=logger)
    shrt.connect_db()

    for mode in modes:
        run(driver, mode)
        connect_and_savejson(mode=mode, try_connect=try_again_loading)
        shrt.action(mode)

    shrt.save_product()
    logger.info("Done")