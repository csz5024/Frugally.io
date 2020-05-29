

import scrapy
from scrapy.http import HtmlResponse
from selenium import webdriver

#options = webdriver.ChromeOptions()
#options.add_argument('headless')
#options.add_argument('window-size=1200x600')

#driver = webdriver.Chrome(executable_path='home/roger/chromedriver.exe', chrome_options=options)



#body = driver.page_source
#return HtmlResponse(driver.current_url, body=body, encoding='utf-8', request=request)

#driver = webdriver.Chrome('home/roger/chromedriver')
#driver.get("https://www.nordstromrack.com/shop/Men/Clothing")

class UrbanOutfittersSpider(scrapy.Spider):
    name = "UrbanOutfitters"
    start_urls = ["https://www.urbanoutfitters.com/mens-clothing"]
    #driver.get(start_urls)

    def parse(self, response):
        numitems = 0
        for article in response.css('div.c-pwa-title-grid-inner'):
            numitems = numitems + 1
            yield{
                'title': article.css('.c-pwa-product-title__heading ::text').get(),
                #'brand': ,
                'retail-price': article.css('..c-pwa-product-price__current span::attr(aria-label)').get(),
                'price': article.css('.c-pwa-product-price__current ::text').get(),
                #'discount': article.css('.product-grid-item__sale-price-discount ::text').get(),
                'image-link': article.css('.c-pwa-product-price__image-outer img::attr(src)').get(),
                'link': article.css('.c-pwa-product-title a::attr(href)').get()
            }
        next_page = response.css('a.pagination-link::attr(href)').get()
        if next_page is not None:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse)
        #driver.execute_script("window.scrollBy(0,document.body.scrollHeight)")
        print(numitems)
