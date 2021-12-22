from bs4.element import SoupStrainer
import requests
from bs4 import BeautifulSoup as bs

session = requests.session()

def get_sizes_in_stock():
    global session
    endpoint = ''
    response = session.get(endpoint)

    soup = bs(response.text,"html.parser")
