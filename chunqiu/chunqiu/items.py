# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ChunqiuItem(scrapy.Item):
    # define the fields for your item here like:
    FromCode = scrapy.Field()
    ToCode = scrapy.Field()
    DateTime = scrapy.Field()
    Value = scrapy.Field()
    
