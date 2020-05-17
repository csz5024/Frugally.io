# -*- coding: utf-8 -*-
import scrapy


class NordstromSpider(scrapy.Spider):
    name = 'nordstrom'
    allowed_domains = ['nordstrom.com']
    start_urls = ['http://nordstrom.com/']

    def parse(self, response):
        pass
