

import scrapy
from scrapy.selector import Selector
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.action_chains import ActionChains


class NordstromRackWomenSpider(scrapy.Spider):
    name = "NordstromRackWomen"
    start_urls = ["https://www.nordstromrack.com/shop/Women/Clothing"]


    def parse(self, response):

        # Loading a chrome window with specific settings

        options = webdriver.ChromeOptions()
        options.add_argument('headless')
        options.add_argument('window-size=1200x900')
        options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')

        self.driver = webdriver.Chrome(executable_path="/home/roger/chromedriver.exe", chrome_options=options)

        # Iterating over the number of pages in Nordstrom Rack

        iter = 1

        while True:
            # Loading each page to extract the data
            url = "https://www.nordstromrack.com/shop/Women/Clothing?page={0}&sort=most_popular"
            self.driver.get(url.format(iter))

            # Finding the next page button, and scrolling to it

            element = self.driver.find_element_by_class_name('pagination__link')

            actions = ActionChains(self.driver)

            actions.move_to_element(element).perform()

            WebDriverWait(self.driver, 2)

            scrapy_selector = Selector(text=self.driver.page_source)

            #Loading each product card

            scraplist = scrapy_selector.css('div.product-grid-item')

            # Loading each image

            data = self.driver.find_element_by_class_name('product-grid')
            imlist = data.find_elements_by_tag_name('img')

            for i in range(0,len(scraplist)):
                article = scraplist[i]
                # Finding the discount of each article and yielding all the data
                discount = article.css('.product-grid-item__sale-price-discount ::text').get()
                if discount is not None:
                    image = imlist[i*2].get_attribute('src')
                    yield {
                        'vendor': 'NordstromRack',
                        'gender': 'Women',
                        'title': article.css('.product-grid-item__title ::text').get(),
                        'brand': article.css('.product-grid-item__brand ::text').get(),
                        'retail-price': article.css('.product-grid-item__retail-price del::text').get(),
                        'price': article.css('.product-grid-item__sale-price ::text').get(),
                        'discount': discount,
                        'image-link': image, #article.css('.product-grid-item__catalog-image img::attr(src)').get(),
                        'link': 'https://nordstormrack.com' + article.css('.product-grid-item a::attr(href)').get()
                }
            iter += 1

            if element is None:
                break
