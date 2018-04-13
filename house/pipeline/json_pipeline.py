# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import json


class JsonWriterPipeline(object):

    def open_spider(self, spider):
        # json
        self.json_file = open('./spiders/data/house.json', 'w')

    def close_spider(self, spider):
        self.json_file.close()

    def process_item(self, item, spider):
        # json
        line = json.dumps(dict(item), ensure_ascii=False) + ",\n"
        self.json_file.write(line)
        return item
