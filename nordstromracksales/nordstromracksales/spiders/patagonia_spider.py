

import scrapy
from scrapy.selector import Selector
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import Select


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

        url = "https://www.patagonia.com/on/demandware.store/Sites-patagonia-us-Site/en_US/Search-UpdateGrid?cgid=web-specials-mens&amp;start=64&amp;sz=1000"
        self.driver.get(url)

        iter = 1

        WebDriverWait(self.driver, 2)

        #last_height = self.driver.execute_script("return document.body.scrollHeight")
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        WebDriverWait(self.driver, 2)

        element = self.driver.find_element_by_xpath('/html/body/div[65]/div[1]/div/button')

        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        actions = ActionChains(self.driver)

        actions.move_to_element(element).perform()

        WebDriverWait(self.driver, 2)

        actions.click(element).perform()
        #element.click()

        WebDriverWait(self.driver, 2)

        last_height = self.driver.execute_script("return document.body.scrollHeight")

        while True:
            numitems = 0\

            WebDriverWait(self.driver, 2)

            print('here')
            #print(element)

            WebDriverWait(self.driver, 2)

            #self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

            WebDriverWait(self.driver, 2)

            scrapy_selector = Selector(text=self.driver.page_source)

            WebDriverWait(self.driver, 2)

            scraplist = scrapy_selector.css('div.product-tile__wrapper')

            for i in range(0,len(scraplist)):
                article = scraplist[i]
                yield {
                    'vendor': 'Patagonia',
                    'title': article.css('h4.product-tile__name ::text').get(),
                    'brand': 'Patagonia',
                    'retail-price': article.css('span.value ::text').getall()[0],
                    'price': article.css('span.value ::text').getall()[1],
                    'discount': None,
                    'image-link': article.css('.product-tile__image img::attr(data-src)').get(),
                    'link': 'https://patagonia.com' + article.css('.product-tile__image a::attr(href)').get()
                }
            iter += 1
            print(iter)

            element.click()

            #if element is None:
            #    print('now')
            #    break
            new_height = self.driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height

            print(numitems)
