

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


class AdidasSpider(scrapy.Spider):
    name = "Adidas"
    start_urls = ["https://www.adidas.com/us/running_promo"]


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

            url = "https://www.adidas.com/us/running_promo"
            self.driver.get(url.format(iter))
            numitems = 0\

            WebDriverWait(self.driver, 2)


            last_height = self.driver.execute_script("return document.body.scrollHeight")
            new_height = 0

            element = self.driver.find_element_by_class_name('gl-cta__content')

            actions = ActionChains(self.driver)

            actions.move_to_element(element).perform()

            print('here')
            print(element)

            WebDriverWait(self.driver, 2)

            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

            WebDriverWait(self.driver, 2)

            scrapy_selector = Selector(text=self.driver.page_source)

            WebDriverWait(self.driver, 2)

            scraplist = scrapy_selector.css('div.gl-product-card')

            data = self.driver.find_element_by_class_name('gl-product-card')
            imlist = data.find_elements_by_tag_name('img')

            for i in range(0,len(response.css('div.gl-product-card'))):
                article = scraplist[i]
                image = imlist[i*2].get_attribute('src')
                yield {
                    'vendor': 'Adidas',
                    'title': article.css('span.gl-label ::text').get(),
                    'brand': 'Adidas',
                    'retail-price': article.css('span.gl-price__value ::text')[0].get(),
                    'price': article.css('span.gl-price__value ::text')[1].get(),
                    'discount': None,
                    'image-link': image, #article.css('.product-grid-item__catalog-image img::attr(src)').get(),
                    'link': article.css('div.gl-product-card a::attr(href)').get()
                }
            iter += 1
            print(iter)

            if element is None:
                print('now')
                break
            print(numitems)
