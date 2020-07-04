

import scrapy
from scrapy.selector import Selector
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.action_chains import ActionChains
import time
import mysql.connector
import json
import sys


class NikeMenSpider(scrapy.Spider):
    name = "NikeMen"
    start_urls = ["https://www.nike.com/w/mens-sale-3yaepznik1"]

    def parse(self, response):

        conn = mysql.connector.connect(
            host="localhost",
            user="frugally",
            password="Shoelas",
            database="Frugally"
        )
        cursor = conn.cursor()

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

            vendor = 'Nike'
            gender = 'Men'
            title = article.css('div.product-card__title ::text').get()
            brand = 'Nike'
            retailprice = article.css('div.css-31z3ik ::text').get()
            price = article.css('div.css-s56yt7 ::text').get()
            discount = None
            imagelink = image
            link = article.css('.product-card__body a::attr(href)').get()

            #This file is a script with no dependencies. It relays the content found in the json files to the database
            #Now supports multiple processes


            print('Adding NikeMens Content to Database, please wait...')

            if((retailprice!=None) and (price!=None)):
              if(len(retailprice)>4):
                  retail = float(retailprice.strip("$").replace(',',''))
              else:
                  retail = float(retailprice.strip("$"))
              if(len(price)>4):
                  price = float(price.strip("$").replace(',',''))
              else:
                  price = float(price.strip("$"))
              discount = round((1-(price/retail))*100)
            else:
              discount = 0
            title = str(title.strip("Nike "))
            sql = 'INSERT INTO NikeMenTemp(vendor, gender, title, brand, retailprice, price, discount, imagelink, link) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s);'
            link = link.strip("https://")
            val =  (str(vendor), str(gender), title, str(brand), retail, price, discount, str(imagelink), link)

            #print("NikeMen item number "+str(count))
            cursor.execute(sql, val)
            conn.commit()

        # Removes Duplicate Rows
        cursor.execute("CREATE TABLE tempNM SELECT DISTINCT * FROM NikeMenTemp;")
        cursor.execute("ALTER TABLE NikeMenTemp RENAME junk;")
        cursor.execute("ALTER TABLE tempNM RENAME NikeMenTemp;")
        cursor.execute("DROP TABLE junk;")

        # Drops old table
        cursor.execute("DROP TABLE IF EXISTS NikeMen;")

        # Swaps in new table
        cursor.execute('ALTER TABLE NikeMenTemp RENAME TO NikeMen;')

        # Replaces old temp tables
        cursor.execute('CREATE TABLE NikeMenTemp LIKE NikeMen;')
        conn.commit()
        print("NikeMens... Done!")

        cursor.close()
        conn.close()