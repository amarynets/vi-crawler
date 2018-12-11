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
            type_ = self.clean_number(type_)
            for i in univ.css('a'):
                name = i.css('::text').extract_first().strip()
                university_item = UniversityItem(
                    id=self.slugify(name),
                    name=name,
                    url=response.urljoin(i.css('::attr(href)').extract_first()),
                    type=type_,
                    region_id=region['id']
                )
                yield scrapy.Request(
                    url=university_item['url'],
                    callback=self.parse_specialty,
                    meta={'university': university_item}
                )

    def parse_specialty(self, response):
        university = response.meta['university']
        university['description'] = '\n'.join(response.xpath('.//table[@id="about"]//text()').extract())
        yield university

        full_time = response.xpath('.//div[contains(@id, "den-")]')
        part_time = response.xpath('.//div[contains(@id, "zao-")]')

        for form, type_of_studding in zip(('Денна', 'Заочна'), [full_time, part_time]):
            if not type_of_studding:
                continue
            degrees = type_of_studding.xpath('.//ul[@id="myTab"]//a')
            for degree in degrees:
                degree_name = self.clean_number(degree.root.text.strip())
                degree_ancor = degree.root.attrib['href']

                for specialty in response.xpath('.//div[@id=$ancor]//a[@class="button button-mini"]/@href', ancor=degree_ancor[1:]).extract():
                    specialty_item = SpecialtyItem(
                        id=specialty.split('/')[-1].split('.html')[0],
                        url=response.urljoin(specialty),
                        degree=degree_name,
                        time=form,
                        university_id=university['id']
                    )
                    yield scrapy.Request(
                        url=specialty_item['url'],
                        callback=self.parse_student_list,
                        meta={'specialty': specialty_item}
                    )

    def parse_student_list(self, response):
        specialty = response.meta['specialty']
        extra_info = response.xpath('.//div[@class="title-page"]//span[@class="search"]//text()').extract()
        extra_info = [i for i in extra_info if i.strip()]
        extra_info = dict([extra_info[i:i+2] for i in range(0, len(extra_info), 2)])
        specialty['name'] = extra_info['Спеціальність:']
        specialty['id'] = self.slugify(extra_info['Спеціальність:'])
        a = 1

