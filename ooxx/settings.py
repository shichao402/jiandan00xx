# -*- coding: utf-8 -*-

# Scrapy settings for scrapy_jiandan project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#
import os


BOT_NAME = 'ooxx'

SPIDER_MODULES = ['ooxx.spiders']
NEWSPIDER_MODULE = 'ooxx.spiders'

ITEM_PIPELINES = {
	'ooxx.pipelines.ooxxDuplicatesPipeline': 100,
	'ooxx.pipelines.MyImagesPipeline': 500,
	'ooxx.pipelines.ooxxPipeline': 600,
}

CONCURRENT_REQUESTS=2
DOWNLOAD_DELAY=3
CONCURRENT_REQUESTS_PER_DOMAIN=2
CONCURRENT_REQUESTS_PER_IP=2

IMAGES_STORE = os.path.split(os.path.realpath(__file__))[0] + os.sep + '..' + os.sep  + '/downloads/images'

IMAGES_MIN_HEIGHT = 100
IMAGES_MIN_WIDTH = 100

COOKIES_ENABLED=True

