

import scrapy


class NordstromRackSpider(scrapy.Spider):
    name = "NordstromRack"
    start_urls = ["https://www.nordstromrack.com/shop/Men/Clothing"]


    def parse(self, response):
        numitems = 0
        for article in response.css('div.product-grid-item'):
            numitems = numitems + 1
            yield{
                'title': article.css('.product-grid-item__title ::text').get(),
                'brand': article.css('.product-grid-item__brand ::text').get(),
                'retail-price': article.css('.product-grid-item__retail-price del::text').get(),
                'price': article.css('.product-grid-item__sale-price ::text').get(),
                'discount': article.css('.product-grid-item__sale-price-discount ::text').get(),
                'image-link': article.css('.product-grid-item__catalog-image img::attr(src)').get(),
                'link': 'https://nordstormrack.com' + article.css('.product-grid-item a::attr(href)').get()
            }
        next_page = response.css('a.pagination__link::attr(href)').get()
        print('here')
        print(next_page)
        if next_page is not None:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse)
        print(numitems)
