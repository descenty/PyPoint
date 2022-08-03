from main_app.models import GoodCategory
import requests

CATEGORIES_URL = 'https://www.wildberries.ru/webapi/menu/main-menu-ru-ru.json'
CATALOG_URL = 'https://catalog.wb.ru/catalog/{category.shard}/catalog?locale=ru&{category.query}'


class Category:
    def __init__(self, id: int, name: str, url: str, shard: str, query: str,
                 parent: int = None, seo: str = None, landing: bool = False,
                 isDenyLink: bool = True, dest: list = None):
        self.id = id
        self.parent = parent
        self.name = name
        self.url = url
        self.shard = shard
        self.query = query
        self.landing = landing


def get_child_categories(category: dict, output: list[Category]) -> None:
    if 'shard' not in category.keys():
        return
    if 'childs' in category.keys():
        for child in category['childs']:
            get_child_categories(child, output)
    category.pop('childs', None)
    output.append(Category(**category))


def parse_categories() -> list[Category]:
    data = requests.get(CATEGORIES_URL).json()
    categories: list[Category] = []
    for category in data:
        children: list[Category] = []
        get_child_categories(category, children)
        categories.extend(children)
    return categories


def load_categories_to_orm():
    categories = parse_categories()
    GoodCategory.objects.all().delete()
    for category in categories:
        GoodCategory.objects.create(
            id=category.id,
            name=category.name,
            url=category.url,
            shard=category.shard,
            query=category.query,
        )
    for category in categories:
        good_category: GoodCategory = GoodCategory.objects.get(pk=category.id)
        good_category.parent_id = category.parent
        good_category.save()
