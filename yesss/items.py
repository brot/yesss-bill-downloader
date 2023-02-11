# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class YesssBillItem(scrapy.Item):
    date = scrapy.Field()
    date_raw = scrapy.Field()
    date_formatted = scrapy.Field()
    bill_sum = scrapy.Field()
    bill_no = scrapy.Field()
    bill_pdf = scrapy.Field()
    egn_pdf = scrapy.Field()
