# -*- coding: utf-8 -*-
import json


class CrawlerPipeline(object):

    def open_spider(self, spider):
        self.file_names = ['RegionItem', 'UniversityItem', 'SpecialtyItem']
        self.files = {k: open(f'{k}.json', 'w', encoding='utf-8') for k in self.file_names}
        for file in self.files.values():
            file.write('[\n')

        self.statuses = {k: True for k in self.file_names}

    def close_spider(self, spider):
        for file in self.files.values():
            file.write('\n]')
            file.close()

    def process_item(self, item, spider):
        if self.statuses[item.__class__.__name__]:
            self.statuses[item.__class__.__name__] = False
            json.dump(dict(item), self.files[item.__class__.__name__], indent=4, ensure_ascii=False)
        else:
            self.files[item.__class__.__name__].write(',\n')
            json.dump(dict(item), self.files[item.__class__.__name__], indent=4, ensure_ascii=False)
        return item
