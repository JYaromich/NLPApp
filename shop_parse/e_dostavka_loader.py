from scrapy import Selector
from scrapy.loader import ItemLoader
from itemloaders.processors import TakeFirst


class EDostavkaLoader(ItemLoader):
    default_item_class = dict
    title_out = TakeFirst()
    name_out = TakeFirst()
    value_out = TakeFirst()
