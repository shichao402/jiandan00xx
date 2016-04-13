# -*- coding: utf-8 -*-
import scrapy
import os
#煎蛋网
from ooxx.items import ooxxItem


class Spider_jiandan(scrapy.Spider):
    name = "ooxx"

    start_urls = [
        "http://jandan.net/ooxx"
    ]

    max_page = 3;

    def __init__(self):
        self.cookies = {
            'bad-click-load':r'off',
            'nsfw-click-load':r'off'
        }

    def parse(self, response):
        item = ooxxItem()
        item['type'] = 0
        item['url'] = response.url
        item['image_urls'] = []
        yield item

        item = ooxxItem()
        preachs=response.xpath('//ol[@class="commentlist"]//div[@class="text"]//a[@class="view_img_link"]')
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