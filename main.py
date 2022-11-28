from selenium import webdriver
from selenium.webdriver.edge.service import Service as EdgeService
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.wait import WebDriverWait
from config import username, userInput_id, passwordInput_id, password, DNAC_Shockwave_Solution, metajson_xpath, login_button_id,\
    trust_browser_button_id, tbody_xpath, information_metajson_xpath, DNAC_Guardian_Solution, log
import logging
from logging import config
import time
import json


log_config = log
config.dictConfig(log_config)
logger = logging.getLogger("root")


def check_exists_byOptions(drivers, option: str, infor: str) -> bool:
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
        logger.error(e)
        return False
    return True


def Login_and_Authenticate(driver) -> bool:
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
        logger.error(e)
        return False
    return True


def DNAC(driver, mode: str):
    if mode == "shockwave":
        driver.get(DNAC_Shockwave_Solution)
    if mode == "guardian":
        driver.get(DNAC_Guardian_Solution)
    try:
        link_href = []
        if not Login_and_Authenticate(driver):
            return "Error"
        if not check_exists_byOptions(driver, "XPATH", tbody_xpath):
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
        logger.error(e)
        return e


def download_metajson(link_href: list, mode: str):
    if not link_href:
        return "Error"
    for index, value in enumerate(link_href):
        driver.get(value)
        try:
            element = WebDriverWait(driver, 60).until(
                EC.presence_of_element_located(
                    (By.XPATH, metajson_xpath))
            )
            element.click()
            element = WebDriverWait(driver, 60).until(
                EC.visibility_of_all_elements_located(
                    (By.XPATH, information_metajson_xpath))
            )
            time.sleep(4)
            text = driver.find_element(
                By.XPATH, information_metajson_xpath).text
            text = eval(text)
            with open('./meta/' + mode + f'/meta ({index}).json', 'w') as outfile:
                json.dump(text, outfile, indent=4, separators=(", ", ": "))
        except:
            pass


def run(driver, mode: str):
    link_herf = DNAC(driver, mode)
    download_metajson(link_herf, mode)


if __name__ == "__main__":
    driver = webdriver.Edge(service=EdgeService(
        EdgeChromiumDriverManager().install()))
    modes = ["shockwave", "guardian"]
    for mode in modes:
        run(driver, mode)
