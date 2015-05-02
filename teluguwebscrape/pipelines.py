# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo
import datetime
import sys
import os
from scrapy.exceptions import DropItem

class InsertMongoPipeline(object):
    words_to_filter = ['sexual','sex','health']

    def __init__(self):

        if os.environ.get("SCRAPY_ENV") == "local":
            connection_string = "mongodb://localhost"
            connection = pymongo.Connection(connection_string, safe=True)
            db = connection.teluguweb
        else:
            connection_string = os.environ["MONGOLAB_URI"]
            connection = pymongo.Connection(connection_string, safe=True)
            db = connection.heroku_app36456202

        self.links = db.links

    def process_item(self, item, spider):

        for word in self.words_to_filter:
            if word in unicode(item['url']).lower():
                raise DropItem("Contains forbidden word: %s" % word)
                return
        if not 'paperweight' in item:
            item['paperweight'] = 10
        if not 'itemweigth' in item:
            item['itemweight'] = 10

        if item['title']:
            time = datetime.time(0,0,0)
            post = {"source": item['source'],
                    "engsource": item['engsource'],
                    "title": item['title'][0],
                    "url": item['url'],
                    #"desc": item['desc'][0],
                    "mindesc": item['mindesc'],
                    "imageurl": item['image_urls'][0],
                    "imagepath": item['image_path'],
                    "insertdatetime": datetime.datetime.utcnow(),
                    "insertdate": datetime.datetime.combine(datetime.datetime.utcnow().date(),time),
                    "weight": item['paperweight'] * item['itemweight']
                }

            if self.findrecord(item['url']):
                return
            else:
                try:
                    print "Inserting the post"
                    self.links.insert(post)
                except:
                    print "Error inserting post"
                    print "Unexpected Error:", sys.exc_info()[0]

        return item


    def findrecord(self, url):
        return self.links.find_one({'url': url})
