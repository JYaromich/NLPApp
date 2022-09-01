from ast import parse
import scrapy
from urllib.parse import urlencode
from shop_parse.e_dostavka_loader import EDostavkaLoader


class EDostavkaSpider(scrapy.Spider):
    name = 'e_dostavka'
    allowed_domains = ['e-dostavka.by']
    _search_url = '/search'
    _xpath_item_filter_query = {
        'title': "//div[@class='item filter_rubric']//div[@class='item_filter']//label/text()[2]",
        'name': "//div[@class='item filter_rubric']//div[@class='item_filter']//label/input/@name",
        'value': "//div[@class='item filter_rubric']//div[@class='item_filter']//label/input/@value"
    }

    def __init__(self, search_item: str,
                 rubric_name: str = None,
                 rubric_value: str = None,
                 *args, **kwargs):

        self.search_item = search_item
        self.rubric_name = rubric_name
        self.rubric_value = rubric_value
        super().__init__(*args, **kwargs)

    def start_requests(self):
        if not self.rubric_name:
            params = {'searchtext': self.search_item}
            urls = [f'http://e-dostavka.by/search/?{urlencode(params)}']

            for url in urls:
                yield scrapy.Request(url=url, callback=self.rubric_parse)

    def rubric_parse(self, response):
        loader = EDostavkaLoader(response=response)
        for key, selector in self._xpath_item_filter_query.items():
            loader.add_xpath(key, selector)
        yield loader.load_item()

# https://e-dostavka.by/search/?searchtext=Апельсин&rubric_filter%5B7998%5D=7998
