# -*- coding: utf-8 -*-

# Scrapy settings for teluguwebscrape project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#
import os

BOT_NAME = 'teluguweb'
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

SPIDER_MODULES = ['teluguwebscrape.spiders']
NEWSPIDER_MODULE = 'teluguwebscrape.spiders'
#ITEM_PIPELINES = {'teluguwebscrape.pipelines.InsertMongoPipeline': 800}

ITEM_PIPELINES = {'teluguwebscrape.imgpipeline.MyImagesPipeline': 1, 'teluguwebscrape.pipelines.InsertMongoPipeline': 800}

#IMAGES_STORE = '/Users/rgummadi/Dropbox/WWW/dev/teluguweb/teluguwebapp/static/images'
#IMAGES_STORE = os.path.join(BASE_DIR, 'teluguwebscrape/images')
IMAGES_STORE = "s3://%s/images/" % os.environ["S3_BUCKET"]

IMAGES_THUMBS = {
    'small': (200, 200),
    'big': (270, 270),
}

AWS_ACCESS_KEY_ID = os.environ["AWS_ACCESS_KEY"]
AWS_SECRET_ACCESS_KEY = os.environ["AWS_SECRET_KEY"]

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'teluguwebscrape (+http://www.yourdomain.com)'
