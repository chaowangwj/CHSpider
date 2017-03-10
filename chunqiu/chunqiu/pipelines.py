# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

# import codecs
# import json

# class ChunqiuPipeline(object):
#     def __init__(self):
#         self.file = codecs.open('items.json', 'w')
#     def process_item(self, item, spider):
#         try:
#             Dict = json.loads(item["CHJson"][1])
#         except Exception as e:
#             pass
#         else:
#             if len(Dict["Route"]) > 0:
#                 saveDict = {item["CHJson"][0]:Dict["Route"]}
#                 jsonStr = json.dumps(saveDict,enumerate=False)
#                 self.file.write(jsonStr+"\n")
#                 return item

import pymongo
import json
class ChunqiuPipeline(object):

    collection_name = 'scrapy_items'

    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri=crawler.settings.get('MONGO_URI'),
            mongo_db=crawler.settings.get('MONGODB_DB', 'items')
        )

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        try:
            Dict = json.loads(item["Value"])
        except Exception as e:
            print e
        else:
            if len(Dict["Route"]) > 0:
                item["Value"] = Dict["Route"]
                # jsonStr = json.dumps(item,ensure_ascii=False)
                # self.file.write(jsonStr+"\n")
                self.db[self.collection_name].insert(dict(item))
                print ">>>>>>>>>>>>>>>>>>>>>>>"
        return item