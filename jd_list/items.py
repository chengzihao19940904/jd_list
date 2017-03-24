# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from sched import scheduler
from scrapy.loader import ItemLoader
from scrapy.loader.processors import MapCompose,TakeFirst,Join


class JdListItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    goods_img = scrapy.Item()
    goods_name = scrapy.Item()
    goods_price = scrapy.Item()
    comment_num = scrapy.Item()

    # pass



class JdListLoader(ItemLoader):
    default_item_class = JdListItem
    default_input_processor = MapCompose(lambda s:s.strip)
    default_output_processor = TakeFirst()
    description_out = Join()
