# -*- coding: utf-8 -*-
import re
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
            yield scrapy.Request(
                url=region_item['url'],
                callback=self.parse_university,
                meta={'region': region_item}
            )

    def parse_university(self, response):
        region = response.meta['region']
        universities = response.xpath('.//div[@id="okrArea"]/div')
        type_of_universities = universities.css('div.accordion-heading a::text').extract()
        list_of_universities = universities.css('div.accordion-body')
        for type_, univ in zip(type_of_universities, list_of_universities):
            type_ = re.sub('(\(\d+\))', '', type_).strip()
            for i in univ.css('a'):
                name = i.css('::text').extract_first().strip()
                university_item = UniversityItem(
                    id=self.slugify(name),
                    name=name,
                    url=response.urljoin(i.css('::attr(href)').extract_first()),
                    type=type_,
                    region_id=region['id']
                )
                yield university_item



