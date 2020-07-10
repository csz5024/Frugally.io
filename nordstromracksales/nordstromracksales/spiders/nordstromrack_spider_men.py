

import scrapy
from scrapy.selector import Selector
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.action_chains import ActionChains
import mysql.connector
import json
import sys

class NordstromRackMenSpider(scrapy.Spider):
    name = "NordstromRackMen"
    start_urls = ["https://www.nordstromrack.com/shop/Men/Clothing"]


    def parse(self, response):

        conn = mysql.connector.connect(
            host="localhost",
            user="frugally",
            password="Shoelas",
            database="Frugally"
        )
        cursor = conn.cursor()

        #Loading a chrome window with specific settings

        options = webdriver.ChromeOptions()
        options.add_argument('headless')
        options.add_argument('window-size=1200x900')
        options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')

        self.driver = webdriver.Chrome(executable_path="/var/www/Frugally/Frugally/chromedriver", chrome_options=options)

        #Iterating over the number of pages in Nordstrom Rack

        iter = 1

        try:
            while True:
                #Loading each page to extract the data
                url = "https://www.nordstromrack.com/shop/Men/Clothing?page={0}&sort=most_popular"
                self.driver.get(url.format(iter))

                #Finding the next page button, and scrolling to it
                element = self.driver.find_element_by_class_name('pagination__link')

                actions = ActionChains(self.driver)

                actions.move_to_element(element).perform()

                WebDriverWait(self.driver, 2)

                scrapy_selector = Selector(text=self.driver.page_source)

                #Loading each product card

                scraplist = scrapy_selector.css('div.product-grid-item')

                #Loading each image

                data = self.driver.find_element_by_class_name('product-grid')
                imlist = data.find_elements_by_tag_name('img')

                for i in range(0,len(scraplist)):
                    article = scraplist[i]
                    #Finding the discount of each article and yielding all the data
                    discount = article.css('.product-grid-item__sale-price-discount ::text').get()
                    if discount is not None:
                        image = imlist[i*2].get_attribute('src')
                        vendor = 'NordstromRack'
                        gender = 'Men'
                        title = article.css('.product-grid-item__title ::text').get()
                        brand = article.css('.product-grid-item__brand ::text').get()
                        retailprice = article.css('.product-grid-item__retail-price del::text').get()
                        price = article.css('.product-grid-item__sale-price ::text').get()
                        discount = discount
                        imagelink = image
                        link = article.css('.product-grid-item a::attr(href)').get()
                        #print('Adding NordstromRackMen Content to Database, please wait...')
                        if (discount != None):
                            disc = discount.split()
                            disc = disc[0].strip('%')
                            disc = int(disc)
                        else:
                            disc = int(0)
                        if (retailprice != None):
                            rprice = retailprice.strip('$')
                            if (len(rprice) > 6):
                                rprice = rprice.replace(',', '')
                            rprice = float(rprice)
                        else:
                            rprice = float(0)
                        if (price != None):
                            price = price.strip('$')
                            if (len(price) > 6):
                                price = price.replace(',', '')
                            price = float(price)
                        else:
                            price = float(0)
                        vendor = "Nordstrom Rack"
                        sql = 'INSERT INTO NordstromRackMenTemp(vendor, gender, title, brand, retailprice, price, discount, imagelink, link) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s);'
                        val = (vendor, str(gender), str(title), str(brand), rprice, price, disc,
                               str(imagelink), str(link))

                        # print("NordstromRackMen item number "+str(count))
                        cursor.execute(sql, val)
                        conn.commit()
                iter += 1

                if element is None:
                    break
        finally:
            # Removes Duplicate Rows
            cursor.execute("CREATE TABLE tempNRM SELECT DISTINCT * FROM NordstromRackMenTemp;")
            cursor.execute("ALTER TABLE NordstromRackMenTemp RENAME junk;")
            cursor.execute("ALTER TABLE tempNRM RENAME NordstromRackMenTemp;")
            cursor.execute("DROP TABLE junk;")

            # Drops old table
            cursor.execute("DROP TABLE IF EXISTS NordstromRackMen;")

            # Swaps in new table
            cursor.execute('ALTER TABLE NordstromRackMenTemp RENAME TO NordstromRackMen;')

            # Replaces old temp tables
            cursor.execute('CREATE TABLE NordstromRackMenTemp LIKE NordstromRackMen;')
            conn.commit()
            print("NordstromRackMens... Done!")

            cursor.close()
            conn.close()

