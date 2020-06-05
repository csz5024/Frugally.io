

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


class AsosSpider(scrapy.Spider):
    name = "Asos"
    start_urls = ["https://www.asos.com/us/men/sale/cat/?cid=8409&nlid=mw|sale|shop+by+product"]


    def parse(self, response):

        options = webdriver.ChromeOptions()
        options.add_argument('headless')
        options.add_argument('window-size=1200x900')
        options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')

        self.driver = webdriver.Chrome(executable_path="/home/roger/chromedriver.exe", chrome_options=options)

        iter = 1

        url = "https://www.asos.com/us/men/sale/cat/?cid=8409&page={0}"
        self.driver.get(url.format(iter))
        numitems = 0

        WebDriverWait(self.driver, 2)

        last_height = self.driver.execute_script("return document.body.scrollHeight")
        new_height = 0

        element = self.driver.find_element_by_class_name('_39qNys')

        actions = ActionChains(self.driver)

        actions.move_to_element(element).perform()

        print('here')
        print(element)

        #WebDriverWait(self.driver, 2)

        #self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        WebDriverWait(self.driver, 2)

        scrapy_selector = Selector(text=self.driver.page_source)

        WebDriverWait(self.driver, 2)

        scraplist = scrapy_selector.xpath('//*[@id="product-9276063"]')

        data = self.driver.find_element_by_class_name('_2qG85dG')
        imlist = data.find_elements_by_tag_name('img')

        for i in range(0, len(response.xpath('//*[@id="product-9276063"]'))):
            article = scraplist[i]
            image = imlist[i].get_attribute('src')
            yield {
                'vendor': 'ASOS',
                'title': article.xpath('//*[@id="product-13907637"]/a/div[2]/div/div/p/text()').get(),
                'brand': None,
                'retail-price': article.xpath('//*[@id="product-13907637"]/a/p/span[1]/text()').get(),
                'price': article.xpath('//*[@id="product-13907637"]/a/p/span[2]/span/text()').get(),
                'discount': article.xpath('//*[@id="product-13907637"]/a/div[3]/text()').get(),
                'image-link': image,  # article.css('.product-grid-item__catalog-image img::attr(src)').get(),
                'link': article.css('._3TqU78D a::attr(href)').get()
            }
        iter += 1
        print(iter)

'''
        while True:

            url = "https://www.asos.com/us/men/sale/cat/?cid=8409&page={0}"
            self.driver.get(url.format(iter))
            numitems = 0\

            WebDriverWait(self.driver, 2)


            last_height = self.driver.execute_script("return document.body.scrollHeight")
            new_height = 0

            element = self.driver.find_element_by_class_name('_39qNys')

            actions = ActionChains(self.driver)

            actions.move_to_element(element).perform()

            print('here')
            print(element)

            WebDriverWait(self.driver, 2)

            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

            WebDriverWait(self.driver, 2)

            scrapy_selector = Selector(text=self.driver.page_source)

            WebDriverWait(self.driver, 2)

            scraplist = scrapy_selector.xpath('//*[@id="product-9276063"]')

            data = self.driver.find_element_by_class_name('_2qG85dG')
            imlist = data.find_elements_by_tag_name('img')

            for i in range(0,len(response.xpath('//*[@id="product-9276063"]'))):
                article = scraplist[i]
                image = imlist[i*2].get_attribute('src')
                yield {
                    'vendor': 'ASOS',
                    'title': article.xpath('//*[@id="product-13907637"]/a/div[2]/div/div/p/text()').get(),
                    'brand': None,
                    'retail-price': article.xpath('//*[@id="product-13907637"]/a/p/span[1]/text()').get(),
                    'price': article.xpath('//*[@id="product-13907637"]/a/p/span[2]/span/text()').get(),
                    'discount': article.xpath('//*[@id="product-13907637"]/a/div[3]/text()').get(),
                    'image-link': image, #article.css('.product-grid-item__catalog-image img::attr(src)').get(),
                    'link': article.css('._3TqU78D a::attr(href)').get()
                }
            iter += 1
            print(iter)

            if element is None:
                print('now')
                break
            print(numitems)
'''