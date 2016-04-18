# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy

from orator import DatabaseManager
from orator import Model
import os
import yaml

DATABASES = yaml.load(open(os.path.split(os.path.realpath(__file__))[0] + os.sep  + '..' + os.sep + 'orator.yml'))['databases']

db = DatabaseManager(DATABASES)
Model.set_connection_resolver(db)

class ooxxModel(Model):
    __table__ = 'ooxx'
    __primary_key__ = "uid"
    __autoincrementing__ = False
    __fillable__ = ["uid", "data"]

class ooxxItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    url = scrapy.Field()
    type = scrapy.Field()
    image_urls = scrapy.Field()
