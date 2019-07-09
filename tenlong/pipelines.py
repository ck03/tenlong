# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json

class TenlongPipeline(object):
    result_list = []
    result_dict = {}

    def process_item(self, item, spider):
        print(item)
        item = dict(item)
        self.result_list.append(item)
        return item

    def close_spider(self, spider):
        self.result_dict["Result"] = self.result_list
        with open("tenlong天瓏.json", "w",
                  encoding="utf-8") as f:
            f.write(json.dumps(dict(self.result_dict), ensure_ascii=False, indent=2))

        print("博客來爬蟲結束.....")
