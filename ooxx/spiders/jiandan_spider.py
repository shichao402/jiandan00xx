# -*- coding: utf-8 -*-
import scrapy
import os
#煎蛋网
from ooxx.items import ooxxItem
from scrapy.http.cookies import CookieJar

class Spider_jiandan(scrapy.Spider):
    name = "ooxx"
    handle_httpstatus_list = [ 403 ] 
    start_urls = [
        "http://jandan.net/ooxx"
    ]

    max_page = 3;

    def __init__(self):
        self.cookies = {
            'bad-click-load':r'on',
            'nsfw-click-load':r'off'
        }


    def parse(self, response):
        if response.status == 403:
            print 'handling 403'
            rebody = scrapy.Selector(text=response.body)
            input_from = rebody.xpath('//input[@name="from"]/@value').extract()[0]
            input_hash = rebody.xpath('//input[@name="hash"]/@value').extract()[0]
            url = "http://www.jandan.net/block.php?action=check_human"
            yield scrapy.FormRequest(url,method="POST",
                    formdata={"from":input_from, "hash":input_hash},
                    callback=self.parse)
            return 
        else:
            item = ooxxItem()
            item['type'] = 0
            item['url'] = response.url
            item['image_urls'] = []
            yield item

            item = ooxxItem()
            preachs=response.xpath('//ol[@class="commentlist"]//div[@class="text"]/p[not(contains(@style,"display:none"))]/a[@class="view_img_link"]')
            for preach in preachs:
                item['type'] = 1
                item['url'] = preach.xpath('@href').extract()[0]
                item['image_urls'] = preach.xpath('@href').extract()
                yield item

            if self.max_page <= 0:
                return

            nextlink=response.xpath('//div[@class="comments"]//a[@class="previous-comment-page"]//@href').extract()

            if nextlink:
                yield scrapy.Request(response.urljoin(nextlink[0]),callback=self.parse )

            self.max_page -= 1


    def handleDetails(self,response):
        jiandan = response.meta['item']

        content = response.xpath('//div[@id="content"]/div[@class="post f"]/p/text()').extract()
        text = ''
        for eachContent in content:
            text += eachContent.strip()
        jiandan['content'] = text

        return jiandan

    
