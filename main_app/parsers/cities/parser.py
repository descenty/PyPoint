import json
from dataclasses import dataclass
from main_app.models import City as CityORM
from main_app.models import Region as RegionORM

path = 'main_app/parsers/cities/russia.json'


@dataclass()
class City:
    region: str
    city: str


def load_cities_to_orm():
    with open(path, encoding='utf-8') as f:
        data = json.load(f)
    regions = set()
    cities = []
    for element in data:
        city: City = City(**element)
        regions.add(city.region)
        cities.append(city)

    CityORM.objects.all().delete()
    RegionORM.objects.all().delete()
    region_id = {}
    for region in regions:
        region_id[region] = RegionORM.objects.create(name=region).id

    city: City
    for city in cities:
        CityORM.objects.create(name=city.city, region_id=region_id[city.region])



