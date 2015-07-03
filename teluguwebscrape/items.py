# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class TeluguwebscrapeItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    itemid = scrapy.Field()
    source = scrapy.Field()
    engsource = scrapy.Field()
    title = scrapy.Field()
    url = scrapy.Field()
    desc = scrapy.Field()
    mindesc = scrapy.Field()
    image_urls = scrapy.Field()
    image_path = scrapy.Field()
    paperweight = scrapy.Field()
    itemweight = scrapy.Field()
    pass
