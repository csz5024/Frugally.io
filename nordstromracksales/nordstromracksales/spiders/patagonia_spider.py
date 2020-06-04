

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


class PatagoniaMenSpider(scrapy.Spider):
    name = "Patagonia"
    start_urls = ["https://www.patagonia.com/shop/web-specials-mens"]


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

            url = "https://www.patagonia.com/shop/web-specials-mens"
            self.driver.get(url)
            numitems = 0\

            WebDriverWait(self.driver, 2)


            last_height = self.driver.execute_script("return document.body.scrollHeight")
            new_height = 0

            #element = self.driver.find_element_by_class_name('button.btn.btn-lg.btn-dark')

            #actions = ActionChains(self.driver)

            #actions.move_to_element(element).perform()

            print('here')
            #print(element)

            WebDriverWait(self.driver, 2)

            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

            WebDriverWait(self.driver, 2)

            scrapy_selector = Selector(text=self.driver.page_source)

            WebDriverWait(self.driver, 2)

            scraplist = scrapy_selector.css('div.product-tile__wrapper')

            data = self.driver.find_element_by_class_name('container.search-results')
            imlist = data.find_elements_by_tag_name('img')

            for i in range(0,len(response.css('div.product-tile__wrapper'))):
                article = scraplist[i]
                image = imlist[i].get_attribute('src')
                yield {
                    'vendor': 'Patagonia',
                    'title': article.css('h4.product-tile__name ::text').get(),
                    'brand': 'Patagonia',
                    'retail-price': article.css('span.strike-through.list ::text').get(),
                    'price': article.css('span.sales ::text').get(),
                    'discount': None,
                    'image-link': article.css('.product-tile__image img::attr(src)').getall(),
                    'link': 'https://patagonia.com' + article.css('.product-tile__image a::attr(href)').get()
                }
            iter += 1
            print(iter)
            break

            #if element is None:
            #    print('now')
            #    break
            print(numitems)
