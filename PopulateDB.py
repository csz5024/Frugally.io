import mysql.connector
import json

'''
This file is a script with no dependencies. It relays the content found in the json files to the database
'''

conn = mysql.connector.connect(
  host="localhost",
  user="frugally",
  password="Shoelas",
  database="Frugally"
)
cursor = conn.cursor()


def populateNordstromTables():
  #conn = mysql.connect()
  #cursor.execute('CREATE TABLE IF NOT EXISTS Nike(NAME CHAR(100), SEX CHAR(1), PRICE CHAR(10))')

  print('clearing tables')
  cursor.execute('TRUNCATE TABLE NordstromRackMen')
  cursor.execute('TRUNCATE TABLE NordstromRackWomen')
  conn.commit()

  with open('/var/www/Frugally/Frugally/nordstromracksales/NordstromRackMen.json') as f:
      data = json.load(f)

  for count, item in enumerate(data):
      if(item['discount'] != None):
          disc = item["discount"].split()
          disc = disc[0]
      else:
          disc = "-0%"
      sql = 'INSERT INTO NordstromRackMen(vendor, gender, title, brand, retailprice, price, discount, imagelink, link) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s);'
      val =  (str(item['vendor']), str(item['gender']), str(item['title']), str(item['brand']), str(item['retail-price']), str(item['price']), str(disc), str(item['image-link']), str(item['link']))

      print("NordstromRackMen item number "+str(count))
      cursor.execute(sql, val)
  conn.commit()

  with open('/var/www/Frugally/Frugally/nordstromracksales/NordstromRackWomen.json') as f:
      data = json.load(f)

  for count, item in enumerate(data):
      if(item['discount'] != None):
          disc = item["discount"].split()
          disc = disc[0]
      else:
          disc = "-0%"
      sql = 'INSERT INTO NordstromRackWomen(vendor, gender, title, brand, retailprice, price, discount, imagelink, link) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s);'
      val =  (str(item['vendor']), str(item['gender']), str(item['title']), str(item['brand']), str(item['retail-price']), str(item['price']), str(disc), str(item['image-link']), str(item['link']))

      print("NordstromRackWomen item number "+str(count))
      cursor.execute(sql, val)
  conn.commit()
  return 0


def populateNikeTables():

  print('clearing tables')
  cursor.execute('TRUNCATE TABLE NikeMen')
  cursor.execute('TRUNCATE TABLE NikeWomen')
  conn.commit()

  with open('/var/www/Frugally/Frugally/nordstromracksales/NikeMen.json') as f:
    data = json.load(f)

  for count, item in enumerate(data):
    if((item["retail-price"]!=None) and (item["price"]!=None)):
            retail = float(item["retail-price"].strip("$"))
            price = float(item["price"].strip("$"))
            discount = round((1-(price/retail))*100)
    else:
            discount = 0
    sql = 'INSERT INTO NikeMen(vendor, gender, title, brand, retailprice, price, discount, imagelink, link) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s);'
    val =  (str(item['vendor']), str(item['gender']), str(item['title']), str(item['brand']), str(item['retail-price']), str(item['price']), str(discount), str(item['image-link']), str(item['link']))

    print("NikeMen item number "+str(count))
    cursor.execute(sql, val)
  conn.commit()
  with open('/var/www/Frugally/Frugally/nordstromracksales/NikeWomen.json') as f:
    data = json.load(f)

  for count, item in enumerate(data):
    if((item["retail-price"]!=None) and (item["price"]!=None)):
            retail = float(item["retail-price"].strip("$"))
            price = float(item["price"].strip("$"))
            discount = round((1-(price/retail))*100)
    else:
            discount = 0
    sql = 'INSERT INTO NikeWomen(vendor, gender, title, brand, retailprice, price, discount, imagelink, link) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s);'
    val =  (str(item['vendor']), str(item['gender']), str(item['title']), str(item['brand']), str(item['retail-price']), str(item['price']), str(discount), str(item['image-link']), str(item['link']))

    print("NikeWomen item number "+str(count))
    cursor.execute(sql, val)
  conn.commit()
  return 0

if __name__=='__main__':
  populateNordstromTables()
  populateNikeTables()
  cursor.close()
  conn.close()
