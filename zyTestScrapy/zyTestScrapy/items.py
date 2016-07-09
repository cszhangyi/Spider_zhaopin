# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

#zy import scrapy
#add
from scrapy.item import Item, Field


class ZytestscrapyItem(Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    # pass
    name = Field()
    detailLink = Field()
    publishTime = Field()
