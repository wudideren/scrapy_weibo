# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

from scrapy import Item, Field


class WeiboScrapingItem(Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    user = Field()
    comment = Field()
    support_number = Field()
    date = Field()


# Caculated fields


# Housekeeping fields

# unit test

