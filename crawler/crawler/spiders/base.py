import re
import scrapy
from slugify import slugify


class BaseSpider(scrapy.Spider):

    @staticmethod
    def slugify(text):
        return slugify(text)

    @staticmethod
    def clean_number(name):
        return re.sub('(\(\d+\))', '', name).strip()
