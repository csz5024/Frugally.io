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

  #print('clearing tables')
  #cursor.execute('TRUNCATE TABLE NordstromRackMen')
  #cursor.execute('TRUNCATE TABLE NordstromRackWomen')
  #conn.commit()

  with open('/var/www/Frugally/Frugally/nordstromracksales/NordstromRackMen.json') as f:
      data = json.load(f)

  print('Adding Nordstrom Content to Database, please wait...')
  for count, item in enumerate(data):
      if(item['discount'] != None):
          disc = item["discount"].split()
          disc = disc[0].strip('%')
          disc = int(disc)
      else:
          disc = int(0)
      if(item['retail-price'] != None):
          rprice = item["retail-price"].strip('$')
          if(len(rprice)>6):
              rprice=rprice.replace(',','')
          rprice = float(rprice)
      else:
          rprice = float(0)
      if(item['price'] != None):
          price = item["price"].strip('$')
          if(len(price)>6):
              price=price.replace(',','')
          price = float(price)
      else:
          price = float(0)
      sql = 'INSERT INTO NordstromRackMenTemp(vendor, gender, title, brand, retailprice, price, discount, imagelink, link) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s);'
      val =  (str(item['vendor']), str(item['gender']), str(item['title']), str(item['brand']), rprice, price, disc, str(item['image-link']), str("nordstromrack.com" + item['link']))

      print("NordstromRackMen item number "+str(count))
      cursor.execute(sql, val)
  conn.commit()

  with open('/var/www/Frugally/Frugally/nordstromracksales/NordstromRackWomen.json') as f:
      data = json.load(f)

  for count, item in enumerate(data):
      if(item['discount'] != None):
          disc = item["discount"].split()
          disc = disc[0].strip('%')
          disc = int(disc)
      else:
          disc = int(0)
      if(item['retail-price'] != None):
          rprice = item["retail-price"].strip('$')
          if(len(rprice)>6):
              rprice=rprice.replace(',','')
          rprice = float(rprice)
      else:
          rprice = float(0)
      if(item['price'] != None):
          price = item["price"].strip('$')
          if(len(price)>6):
              price=price.replace(',','')
          price = float(price)
      else:
          price = float(0)
      sql = 'INSERT INTO NordstromRackWomenTemp(vendor, gender, title, brand, retailprice, price, discount, imagelink, link) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s);'
      val =  (str(item['vendor']), str(item['gender']), str(item['title']), str(item['brand']), rprice, price, disc, str(item['image-link']), str("nordstromrack.com" + item['link']))

      print("NordstromRackWomen item number "+str(count))
      cursor.execute(sql, val)
  conn.commit()
  return 0


def populateNikeTables():

  #print('clearing tables')
  #cursor.execute('TRUNCATE TABLE NikeMen')
  #cursor.execute('TRUNCATE TABLE NikeWomen')
  #conn.commit()

  with open('/var/www/Frugally/Frugally/nordstromracksales/NikeMen.json') as f:
    data = json.load(f)

  if(data != None):
    print('Adding Nike Content to Database, please wait...')
    for count, item in enumerate(data):
      if((item["retail-price"]!=None) and (item["price"]!=None)):
              if(len(item["retail-price"])>4):
                  retail = float(item["retail-price"].strip("$").replace(',',''))
              else:
                  retail = float(item["retail-price"].strip("$"))
              if(len(item["price"])>4):
                  price = float(item["price"].strip("$").replace(',',''))
              else:
                  price = float(item["price"].strip("$"))
              discount = round((1-(price/retail))*100)
      else:
              discount = 0
      title = str(item['title'].strip("Nike "))
      sql = 'INSERT INTO NikeMenTemp(vendor, gender, title, brand, retailprice, price, discount, imagelink, link) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s);'
      link = item['link'].strip("https://") 
      val =  (str(item['vendor']), str(item['gender']), title, str(item['brand']), retail, price, discount, str(item['image-link']), link)

      print("NikeMen item number "+str(count))
      cursor.execute(sql, val)
    conn.commit()

  with open('/var/www/Frugally/Frugally/nordstromracksales/NikeWomen.json') as f:
    data = json.load(f)

  for count, item in enumerate(data):
    if((item["retail-price"]!=None) and (item["price"]!=None)):
            if(len(item["retail-price"])>4):
                retail = float(item["retail-price"].strip("$").replace(',',''))
            else:
                retail = float(item["retail-price"].strip("$"))
            if(len(item["price"])>4):
                price = float(item["price"].strip("$").replace(',',''))
            else:
                price = float(item["price"].strip("$"))
            discount = round((1-(price/retail))*100)
    else:
            discount = 0
    title = str(item['title'].strip("Nike "))
    sql = 'INSERT INTO NikeWomenTemp(vendor, gender, title, brand, retailprice, price, discount, imagelink, link) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s);'
    link = item['link'].strip("https://") 
    val =  (str(item['vendor']), str(item['gender']), str(item['title']), str(item['brand']), retail, price, discount, str(item['image-link']), link)

    print("NikeWomen item number "+str(count))
    cursor.execute(sql, val)
  conn.commit()
  return 0

def swapTables():
  print("Dropping old tables...")
  cursor.execute('DROP TABLE IF EXISTS NordstromRackMen, NordstromRackWomen, NikeMen, NikeWomen;')
  print("Swapping in new tables...")
  cursor.execute('ALTER TABLE NordstromRackMenTemp RENAME TO NordstromRackMen;')
  cursor.execute('ALTER TABLE NordstromRackWomenTemp RENAME TO NordstromRackWomen;')
  cursor.execute('ALTER TABLE NikeMenTemp RENAME TO NikeMen;')
  cursor.execute('ALTER TABLE NikeWomenTemp RENAME TO NikeWomen;')
  print("Adding new temp tables...")
  cursor.execute('CREATE TABLE NordstromRackMenTemp LIKE NordstromRackMen;')
  cursor.execute('CREATE TABLE NordstromRackWomenTemp LIKE NordstromRackWomen;')
  cursor.execute('CREATE TABLE NikeMenTemp LIKE NikeMen;')
  cursor.execute('CREATE TABLE NikeWomenTemp LIKE NikeWomen;')
  print("Done!")
  conn.commit()
  return 0

if __name__=='__main__':
  populateNordstromTables()
  populateNikeTables()
  swapTables()
  cursor.close()
  conn.close()
