# -*- coding: utf-8 -*-
import scrapy


class VstupInfoSpider(scrapy.Spider):
    name = 'vstup_info'
    allowed_domains = ['vstup.info']
    start_urls = ['http://vstup.info/']

    def parse(self, response):
        pass
