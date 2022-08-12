import sys
import requests
import pickle
from os.path import exists
from bs4 import BeautifulSoup
from main_app.models import PickPoint, City

COMPANY_URL = 'https://naitiko.ru/companies/wildberries'

CITY_URLS_PATH = 'main_app/parsers/addresses/city_urls.pickle'


def get_cities_urls() -> dict:
    if exists(CITY_URLS_PATH):
        with open(CITY_URLS_PATH, 'rb') as f:
            return pickle.load(f)
    page = requests.get(COMPANY_URL)
    soup = BeautifulSoup(page.text, 'html.parser')
    a_block = soup.find(id='branches')
    cities = {a.text: a['href'] for a in a_block.findAll('a')}
    with open(CITY_URLS_PATH, 'wb') as f:
        pickle.dump(cities, f)
    return cities


def load_pick_points_to_orm(city: str):
    if not City.objects.filter(name=city).exists():
        print(f'город {city} не найден в базе данных', file=sys.stderr)
    cities_urls: dict = get_cities_urls()
    if city not in cities_urls.keys():
        print(f'город {city} не найден', file=sys.stderr)
        return
    page = requests.get(cities_urls[city])
    soup = BeautifulSoup(page.text, 'html.parser')
    addresses = [address_title.findNext("a").text.replace('\xa0', ' ') for address_title in soup.findAll(class_='address_title')]

    for address in addresses:
        if not PickPoint.objects.filter(address=address).exists():
            PickPoint.objects.create(city=City.objects.get(name=city), address=address)
