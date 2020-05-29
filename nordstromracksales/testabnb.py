"""
python3.6
ipython console test
"""
from time import sleep
import selenium
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

header = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36'}

driver = webdriver.Chrome('path/to/chromedriver')
#home page
search_city = driver.find_element_by_xpath('//*[@type="text"]').send_keys('Dubai h\ue007')
sleep(0.8)
search_button = driver.find_element_by_xpath('//*[@type="submit"]')
search_button.click()
sleep(8.7)
#homes vs experiences page
homes_button = driver.find_element_by_xpath('//*[@data-veloute="explore-nav-card:/homes"]')
homes_button.click()
sleep(4.2)
#catalogue page with an
#infinite scroll
last_height = driver.execute_script("return document.body.scrollHeight")
SCROLL_PAUSE_TIME = 7
while True:
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    sleep(SCROLL_PAUSE_TIME)
    new_height = driver.execute_script("return document.body.scrollHeight")
    if new_height == last_height:
        break
    last_height = new_height
    sleep(1.2)