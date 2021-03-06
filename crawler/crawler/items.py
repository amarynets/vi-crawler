# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class RegionItem(scrapy.Item):
    id = scrapy.Field()
    name = scrapy.Field()
    url = scrapy.Field()


class UniversityItem(scrapy.Item):
    id = scrapy.Field()
    name = scrapy.Field()
    url = scrapy.Field()
    type = scrapy.Field()
    description = scrapy.Field()
    region_id = scrapy.Field()


class SpecialtyItem(scrapy.Item):
    id = scrapy.Field()
    name = scrapy.Field()
    url = scrapy.Field()
    degree = scrapy.Field()
    time = scrapy.Field()
    student_list = scrapy.Field()
    university_id = scrapy.Field()

