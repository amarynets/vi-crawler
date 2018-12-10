# -*- coding: utf-8 -*-
import scrapy

from crawler.spiders.base import BaseSpider

from crawler.items import (
    RegionItem,
    UniversityItem,
    SpecialtyItem,
)


class VstupInfoSpider(BaseSpider):
    name = 'vstup_info'
    allowed_domains = ['vstup.info']
    start_urls = ['http://vstup.info/']

    def parse(self, response):
        regions = response.xpath('.//table[@id="2018abet"]//a[contains(@href, ".html")]')
        for region in regions:
            name = region.css('::text').extract_first().strip()
            region_item = RegionItem(
                id=self.slugify(name),
                name=name,
                url=response.urljoin(region.css('::attr(href)').extract_first())
            )
            yield region_item
