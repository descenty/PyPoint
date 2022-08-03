import dataclasses
import requests
import pickle
from os.path import exists
from bs4 import BeautifulSoup

COMPANY_URL = 'https://naitiko.ru/companies/wildberries'

CITY_URLS_PATH = 'main_app/parsers/addresses/city_urls.pickle'


@dataclasses.dataclass
class CityUrl:
    name: str
    url: str


def get_cities() -> list[CityUrl]:
    if exists(CITY_URLS_PATH):
        with open(CITY_URLS_PATH, 'rb') as f:
            return pickle.load(f)
    page = requests.get(COMPANY_URL)
    soup = BeautifulSoup(page.text, 'html.parser')
    a_block = soup.find(id='branches')
    cities = [CityUrl(a.text, a['href']) for a in a_block.findAll('a')]
    with open(CITY_URLS_PATH, 'wb') as f:
        pickle.dump(cities, f)
    return cities


def load_pick_points_to_orm(city: str):
    pass