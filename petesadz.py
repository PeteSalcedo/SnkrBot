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


