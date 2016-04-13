import pickle
from scrapy.exceptions import DropItem
from scrapy.xlib.pydispatch import dispatcher
from scrapy import signals
from scrapy.contrib.pipeline.images import ImagesPipeline  
from scrapy import Request
import os


class ooxxPipeline(object):
    def process_item(self, item, spider):
        return item
        
class ooxxDuplicatesPipeline(object):
    dumplicate_file = os.path.split(os.path.realpath(__file__))[0] + os.sep + '..' + os.sep + "dumplicate.txt"

    def __init__(self):
        try:
            self.ids_seen = pickle.load(open(self.dumplicate_file, "r"))
        except:
            self.ids_seen = set()
        
        dispatcher.connect(self.on_spider_closed, signal=signals.spider_closed)

    def on_spider_closed(self, spider, reason):
        pickle.dump(self.ids_seen, open(self.dumplicate_file, "w"))

    def process_item(self, item, spider):
        if item['url'] in self.ids_seen:
            raise DropItem("Duplicate item found: %s" % item)
        else:
            self.ids_seen.add(item['url'])
            return item

class MyImagesPipeline(ImagesPipeline):  
    def file_path(self, request, response=None, info=None):  
        image_guid = request.url.split('/')[-1]  
        return 'full/%s' % (image_guid)  

    def get_media_requests(self, item, info):  
        for image_url in item['image_urls']:  
            yield Request(image_url)  

    def item_completed(self, results, item, info):  
        image_paths = [x['path'] for ok, x in results if ok]  
        if not image_paths:  
            raise DropItem("Item contains no images")  
        return item