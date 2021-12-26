import os
import sys
import six
import pause
import requests
import argparse
import logging.config
from selenium import webdriver
from dateutil import parser as date_parser
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC

"""
This is an experimental script which attempts at utilizing some Nike APIs.
Current implementation:
    1. Login with Selenium
    2. Using the driver's stored cookies, make a Nike API request to add the desired item to your cart
    3. Load the checkout page and place an order
    
Not sure if this will be any faster than the other script...
"""


logging.config.dictConfig({
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "default": {
            "format": "%(asctime)s [PID %(process)d] [Thread %(thread)d] [%(levelname)s] [%(name)s] %(message)s"
        }
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "level": "INFO",
            "formatter": "default",
            "stream": "ext://sys.stdout"
        }
    },
    "root": {
        "level": "INFO",
        "handlers": [
            "console"
        ]
    }
})

NIKE_HOME_URL = "https://www.nike.com/us/en_us/"
NIKE_CHECKOUT_URL = "https://www.nike.com/checkout"
NIKE_CART_API_URL = "https://secure-store.nike.com/us/services/jcartService"
LOGGER = logging.getLogger()


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
        LOGGER.exception("Failed to login: " + str(e))
        six.reraise(Exception, e, sys.exc_info()[2])

    if release_time:
        LOGGER.info("Waiting until release time: " + release_time)
        pause.until(date_parser.parse(release_time))

    num_retries_attempted = 0
    while True:
        try:
            try:
                LOGGER.info("Adding item to cart")
                add_item_to_cart(driver=driver, product_id=product_id, sku_id=sku_id, size=shoe_size)
            except Exception as e:
                LOGGER.exception("Failed to add item to cart " + str(e))
                six.reraise(Exception, e, sys.exc_info()[2])

            try:
                LOGGER.info("Requesting page: " + NIKE_CHECKOUT_URL)
                driver.get(NIKE_CHECKOUT_URL)
            except TimeoutException:
                LOGGER.info("Page load timed out but continuing anyway")

            if purchase:
                try:
                    click_place_order_button(driver=driver)
                except Exception as e:
                    LOGGER.exception("Failed to click place order button: " + str(e))
                    six.reraise(Exception, e, sys.exc_info()[2])

            LOGGER.info("Purchased shoe")
            break
        except Exception:
            if num_retries and num_retries_attempted < num_retries:
                num_retries_attempted += 1
                continue
            else:
                break

    if screenshot_path:
        LOGGER.info("Saving screenshot")
        driver.save_screenshot(screenshot_path)

    driver.quit()

def login(driver, username, password):
    try:
        LOGGER.info("Requesting page: " + NIKE_HOME_URL)
        driver.get(NIKE_HOME_URL)
    except TimeoutException:
        LOGGER.info("Page load timed out but continuing anyway")

    LOGGER.info("Waiting for login button to become clickable")
    wait_until_clickable(driver=driver, xpath="//li[@js-hook='exp-join-login']/button")

    LOGGER.info("Clicking login button")
    driver.find_element_by_xpath("//li[@js-hook='exp-join-login']/button").click()

    LOGGER.info("Waiting for login fields to become visible")
    wait_until_visible(driver=driver, xpath="//input[@name='emailAddress']")

    LOGGER.info("Entering username and password")
    email_input = driver.find_element_by_xpath("//input[@name='emailAddress']")
    email_input.clear()
    email_input.send_keys(username)
    password_input = driver.find_element_by_xpath("//input[@name='password']")
    password_input.clear()
    password_input.send_keys(password)

    LOGGER.info("Logging in")
    driver.find_element_by_xpath("//input[@value='LOG IN']").click()
    wait_until_visible(driver=driver, xpath="//span[text()='My Account']")

    LOGGER.info("Successfully logged in")


def click_place_order_button(driver):
    xpath = "//button[text()='Place order']"

    LOGGER.info("wiating for order buton to become clickable")
    wait_until_clickable(driver, xpath=xpath, duration=20)

    LOGGER.info("clicking place order button")
    driver.find_element_by_xpath(xpath).click()


    