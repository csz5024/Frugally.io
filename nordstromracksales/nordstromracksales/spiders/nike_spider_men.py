

import scrapy
from scrapy.selector import Selector
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.action_chains import ActionChains
import time


class NikeMenSpider(scrapy.Spider):
    name = "NikeMen"
    start_urls = ["https://www.nike.com/w/mens-sale-3yaepznik1"]


    def parse(self, response):

        options = webdriver.ChromeOptions()
        options.add_argument('headless')
        options.add_argument('window-size=1200x900')
        options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')

        self.driver = webdriver.Chrome(executable_path="/home/roger/chromedriver.exe", chrome_options=options)

        url = "https://www.nike.com/w/mens-sale-3yaepznik1"
        self.driver.get(url)

        last_height = self.driver.execute_script("return document.body.scrollHeight")

        while True:

            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

            scrapy_selector = Selector(text=self.driver.page_source)

            WebDriverWait(self.driver, 2)

            scraplist = scrapy_selector.css('div.product-card__body')

            data = self.driver.find_element_by_class_name('product-grid')
            imlist = data.find_elements_by_tag_name('img')

            time.sleep(4)

            new_height = self.driver.execute_script("return document.body.scrollHeight")

            if new_height == last_height:
                break
            last_height = new_height

        for i in range(0, len(scraplist)):
            article = scraplist[i]
            image = imlist[i].get_attribute('src')
            yield {
                'vendor': 'Nike',
                'gender': 'Men',
                'title': article.css('div.product-card__title ::text').get(),
                'brand': 'Nike',
                'retail-price': article.css('div.css-31z3ik ::text').get(),
                'price': article.css('div.css-s56yt7 ::text').get(),
                'discount': None,
                'image-link': image,  # article.css('.product-grid-item__catalog-image img::attr(src)').get(),
                'link': article.css('.product-card__body a::attr(href)').get()
            }
