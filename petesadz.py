from logging import Logger
import os 
import sys
import six
import pause
import requests
import argparse
import logging.config

from selenium import webdriver
from deteutil import parser as date_parser
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC

logging.config.dictConfig({
    "version":1,
    "disable_existing_loggers":False,
    "formatters":{
        "default": {
            "format":"%(asctime)s [PID %(process)d] [Thread %(thread)d] [%(levelname)s] [%(name)s] %(message)s"
        }
    },
    "handlers":{
        "console":{
            "class":"logging.StreamHandler",
            "level":"INFO",
            "formatter":"default",
            "stream":"ext://sys.stdout"
        }
    },
    "root": {
        "level":"INFO",
        "handlers":[
            "console"
        ]
    }
})


NIKE_HOME_URL = "https://www.nike.com/us/en_us/"
NIKE_CHECKOUT_URL = "https://www.nike.com/checkout"
NIKE_CART_API_URL = "https://secure-store.nike.com/us/services/jcartService"

LOGGER = logging.gerLogger()

def run(driver, username, password, product_id, sku_id, shoe_size, login_time=None, release_time=None,
        page_load_timeout=None, screenshot_path=None, purchase=False, num_retries=None):
    driver.maximize_window()
    driver.set_page_load_timeout(page_load_timeout)

    if login_time:
        LOGGER.info("Waiting until login time: " + login_time)
        pause.until(date_parser.parse(login_time))

    try:
        login(driver=driver, username=username, password=password)
    except Exception as e:
        LOGGER.exception('failed to log in:' + str(e))
        six.reraise(Exception, e, sys.exc_info()[2])

    if release_time:
        LOGGER.info("Waitting until release time: " + release_time)
        pause.unil(date_parser.parse(release_time))

    num_retries_attempted = 0
    while True:
        try:
            try:
                LOGGER.info("Adding item to cart")
                add_item_to_cart

