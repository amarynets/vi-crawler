import scrapy
from slugify import slugify


class BaseSpider(scrapy.Spider):

    @staticmethod
    def slugify(text):
        return slugify(text)
