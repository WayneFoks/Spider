# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import csv
from scrapy.exporters import CsvItemExporter


class CsvWriterPipeline(object):

    def open_spider(self, spider):
        self.csv_file = open('./spiders/data/house.csv', 'w')
        self.exporter = CsvItemExporter(self.csv_file, 'utf-8')
        self.exporter.start_exporting()

    def close_spider(self, spider):
        self.exporter.finish_exporting()
        self.csv_file.close()

    def process_item(self, item, spider):
        # csv
        print("################" + str(item))
        self.exporter.export_item(str(item))
        return item
