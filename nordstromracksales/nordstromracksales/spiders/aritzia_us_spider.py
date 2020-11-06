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


class AritziaUSSpider(scrapy.Spider):
  name = "AritziaUS"
  start_urls = ["https://www.aritzia.com/us/en/sale"]

  def parse(self, response):

      conn = mysql.connector.connect(
          host="localhost",
          user="frugally",
          password="Shoelas20",
          database="Frugally"
      )
      cursor = conn.cursor()
      pid = 0

      options = webdriver.ChromeOptions()
      options.add_argument('headless')
      options.add_argument('window-size=1200x900')
      options.add_argument('--headless')
      options.add_argument('--no-sandbox')
      options.add_argument('--disable-dev-shm-usage')

      self.driver = webdriver.Chrome(executable_path="/var/www/Frugally/Frugally/chromedriver", chrome_options=options)

      url = "https://www.aritzia.com/us/en/sale"
      self.driver.get(url)

      last_height = self.driver.execute_script("return document.body.scrollHeight")

      try:
          while True:

              self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

              scrapy_selector = Selector(text=self.driver.page_source)

              WebDriverWait(self.driver, 2)

              scraplist = scrapy_selector.css('div.product-tile')

              data = self.driver.find_element_by_class_name('search-result-items')
              imlist = data.find_elements_by_tag_name('img')

              time.sleep(4)

              new_height = self.driver.execute_script("return document.body.scrollHeight")

              if new_height == last_height:
                  break
              last_height = new_height

          for i in range(0, len(scraplist)):
              article = scraplist[i]
              image = imlist[i].get_attribute('src')

              vendor = 'Aritzia'
              gender = 'Women'
              title = article.css('div.product-name ::text').get()
              brand = article.css('div.product-brand ::text').get()
              retailprice = article.css('div.strike.dib ::text').get()
              price = article.css('div.js-product__sales-price.red ::text').get()
              discount = None
              imagelink = image
              link = article.css('.relative.db.js-plp-hash a::attr(href)').get()

              # This file is a script with no dependencies. It relays the content found in the json files to the database
              # Now supports multiple processes

              print('Adding Aritzia Content to Database, please wait...')

              if ((retailprice != None) and (price != None)):
                  if (len(retailprice) > 4):
                      retailprice = float(retailprice.strip("$").replace(',', ''))
                  else:
                      retailprice = float(retailprice.strip("$"))
                  if (len(price) > 4):
                      price = float(price.strip("$").replace(',', ''))
                  else:
                      price = float(price.strip("$"))
                  discount = round((1 - (price / retailprice)) * 100)
              else:
                  discount = 0
                  retailprice = 0
                  price = 0
                  #continue
              #title = str(title.strip("Nike "))
              sql = 'INSERT INTO AritziaTemp(PID, vendor, gender, title, brand, retailprice, price, discount, imagelink, link) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s);'
              #link = link.strip("https://")
              val = (pid, str(vendor), str(gender), title, str(brand), retailprice, price, discount, str(imagelink), link)

              # print("NikeMen item number "+str(count))
              cursor.execute(sql, val)
              conn.commit()
              pid = pid + 1

      finally:
          # Removes Duplicate Rows
          cursor.execute("CREATE TABLE tempA SELECT * FROM AritziaTemp GROUP BY link;")
          cursor.execute("ALTER TABLE AritziaTemp RENAME junk;")
          cursor.execute("ALTER TABLE tempA RENAME AritziaTemp;")
          cursor.execute("DROP TABLE junk;")

          # Drops old table
          cursor.execute("DROP TABLE IF EXISTS Aritzia;")

          # Swaps in new table
          cursor.execute('ALTER TABLE AritziaTemp RENAME TO Aritzia;')

          # Replaces old temp tables
          cursor.execute('CREATE TABLE AritziaTemp LIKE Aritzia;')
          conn.commit()
          print("Artizia... Done!")

          cursor.close()
          conn.close()
