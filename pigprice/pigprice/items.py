# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class PigpriceItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()

    p_date = scrapy.Field()
    p_province = scrapy.Field()
    p_region = scrapy.Field()
    p_meat_type = scrapy.Field()
    p_price = scrapy.Field()
    