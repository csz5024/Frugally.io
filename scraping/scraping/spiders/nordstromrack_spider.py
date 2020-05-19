import scrapy
from scrapy.http import HtmlResponse
from selenium import webdriver

options = webdriver.ChromeOptions()
options.add_argument('headless')
options.add_argument('window-size=1200x600')

driver = webdriver.Chrome(executable_path="C:\\valuables\\chromedriver.exe", chrome_options=options)

# body = driver.page_source
# return HtmlResponse(driver.current_url, body=body, encoding='utf-8', request=request)

# driver = webdriver.Chrome('home/roger/chromedriver')
driver.get("https://www.nordstromrack.com/shop/Men/Clothing")


class NordstromRackSpider(scrapy.Spider):
    name = "NordstromRack"
    start_urls = "https://www.nordstromrack.com/shop/Men/Clothing"
    driver.get(start_urls)

    def parse(self, response):
        numitems = 0
        for article in response.css('div.product-grid-item'):
            numitems = numitems + 1
            yield {
                'title': article.css('.product-grid-item__title ::text').get(),
                'brand': article.css('.product-grid-item__brand ::text').get(),
                'retail-price': article.css('.product-grid-item__retail-price del::text').get(),
                'price': article.css('.product-grid-item__sale-price ::text').get(),
                'discount': article.css('.product-grid-item__sale-price-discount ::text').get(),
                'image-link': article.css('.product-grid-item__catalog-image img::attr(src)').get(),
                'link': article.css('.product-grid-item a::attr(href)').get()
            }
        next_page = response.css('a.pagination-link::attr(href)').get()
        if next_page is not None:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse)
        driver.execute_script("window.scrollBy(0,document.body.scrollHeight)")
        print(numitems)
