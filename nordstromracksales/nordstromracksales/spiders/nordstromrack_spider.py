

import scrapy
from scrapy.selector import Selector
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.action_chains import ActionChains


options = webdriver.ChromeOptions()
options.add_argument('headless')
options.add_argument('window-size=1200x900')
options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')

driver = webdriver.Chrome(executable_path="/home/roger/chromedriver.exe", chrome_options=options)


class NordstromRackSpider(scrapy.Spider):
    name = "NordstromRack"
    start_urls = ["https://www.nordstromrack.com/shop/Men/Clothing"]


    def parse(self, response):


        options = webdriver.ChromeOptions()
        options.add_argument('headless')
        options.add_argument('window-size=1200x900')
        options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')

        self.driver = webdriver.Chrome(executable_path="/home/roger/chromedriver.exe", chrome_options=options)

        iter = 1

        while True:

            url = "https://www.nordstromrack.com/shop/Men/Clothing?page={0}&sort=most_popular"
            self.driver.get(url.format(iter))
            numitems = 0\

            WebDriverWait(self.driver, 2)


            last_height = self.driver.execute_script("return document.body.scrollHeight")
            new_height = 0

            element = self.driver.find_element_by_class_name('pagination__link')

            actions = ActionChains(self.driver)

            actions.move_to_element(element).perform()

            print('here')
            print(element)

            WebDriverWait(self.driver, 2)

            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

            WebDriverWait(self.driver, 2)

            scrapy_selector = Selector(text=self.driver.page_source)

            WebDriverWait(self.driver, 2)

            scraplist = scrapy_selector.css('div.product-grid-item')

            data = self.driver.find_element_by_class_name('product-grid')
            imlist = data.find_elements_by_tag_name('img')

            for i in range(0,len(response.css('div.product-grid-item'))):
                article = scraplist[i]
                image = imlist[i*2].get_attribute('src')
                yield {
                    'title': article.css('.product-grid-item__title ::text').get(),
                    'brand': article.css('.product-grid-item__brand ::text').get(),
                    'retail-price': article.css('.product-grid-item__retail-price del::text').get(),
                    'price': article.css('.product-grid-item__sale-price ::text').get(),
                    'discount': article.css('.product-grid-item__sale-price-discount ::text').get(),
                    'image-link': image, #article.css('.product-grid-item__catalog-image img::attr(src)').get(),
                    'link': 'https://nordstormrack.com' + article.css('.product-grid-item a::attr(href)').get()
                }
            iter += 1
            print(iter)

            if element is None:
                print('now')
                break

