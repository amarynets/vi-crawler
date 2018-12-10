# -*- coding: utf-8 -*-
import scrapy

from crawler.crawler.spiders.base import BaseSpider


class VstupInfoSpider(BaseSpider):
    name = 'vstup_info'
    allowed_domains = ['vstup.info']
    start_urls = ['https://vstup.info/']

    def parse(self, response):
        regions = response.css('table.table.tablesaw.tablesaw-stack a')
