import requests
from bs4 import BeautifulSoup
from datetime import datetime

if __name__ == '__main__':
	start = datetime.now()
	page = requests.get("https://www.nordstromrack.com/shop/product/3009862/stone-rose-tech-knit-geometric-print-shirt?color=NAVY")
	#page = requests.get("https://www.nordstromrack.com/shop/product/2693143/ben-sherman-end-on-end-plaid-print-short-sleeve-regular-f-it-shirt?color=DARK%20GREEN")
	soup = BeautifulSoup(page.content, 'html.parser')
	print(len(soup.find_all("div", class_="status-badge--sold-out")))
	print(datetime.now()-start)
	#print(soup.prettify())
