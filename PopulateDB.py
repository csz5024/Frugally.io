import mysql.connector
import json
import sys

'''
This file is a script with no dependencies. It relays the content found in the json files to the database

Now supports multiple processes
'''

conn = mysql.connector.connect(
  host="localhost",
  user="frugally",
  password="Shoelas",
  database="Frugally"
)
cursor = conn.cursor()


def populateNordstromRackMenTables():

  with open('/var/www/Frugally/Frugally/nordstromracksales/NordstromRackMen.json') as f:
      data = json.load(f)

  print('Adding NordstromRackMens Content to Database, please wait...')
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
      vendor = "Nordstrom Rack"
      sql = 'INSERT INTO NordstromRackMenTemp(vendor, gender, title, brand, retailprice, price, discount, imagelink, link) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s);'
      val =  (vendor, str(item['gender']), str(item['title']), str(item['brand']), rprice, price, disc, str(item['image-link']), str("nordstromrack.com" + item['link']))

      #print("NordstromRackMen item number "+str(count))
      cursor.execute(sql, val)
  conn.commit()

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
  return 0


def populateNordstromRackWomenTables():

  with open('/var/www/Frugally/Frugally/nordstromracksales/NordstromRackWomen.json') as f:
      data = json.load(f)

  print('Adding NordstromRackWomens Content to Database, please wait...')
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
      vendor = "Nordstrom Rack"
      sql = 'INSERT INTO NordstromRackWomenTemp(vendor, gender, title, brand, retailprice, price, discount, imagelink, link) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s);'
      val =  (vendor, str(item['gender']), str(item['title']), str(item['brand']), rprice, price, disc, str(item['image-link']), str("nordstromrack.com" + item['link']))

      #print("NordstromRackWomen item number "+str(count))
      cursor.execute(sql, val)
  conn.commit()


  # Removes Duplicate Rows
  cursor.execute("CREATE TABLE tempNRW SELECT DISTINCT * FROM NordstromRackWomenTemp;")
  cursor.execute("ALTER TABLE NordstromRackWomenTemp RENAME junk;")
  cursor.execute("ALTER TABLE tempNRW RENAME NordstromRackWomenTemp;")
  cursor.execute("DROP TABLE junk;")

  # Drops old table
  cursor.execute("DROP TABLE IF EXISTS NordstromRackWomen;")

  # Swaps in new table
  cursor.execute('ALTER TABLE NordstromRackWomenTemp RENAME TO NordstromRackWomen;')

  # Replaces old temp tables
  cursor.execute('CREATE TABLE NordstromRackWomenTemp LIKE NordstromRackWomen;')
  conn.commit()
  print("NordstromRackWomens... Done!")
  return 0


def populateNikeMenTables():

  print('Adding NikeMens Content to Database, please wait...')
  with open('/var/www/Frugally/Frugally/nordstromracksales/NikeMen.json') as f:
    data = json.load(f)

  if(data != None):
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
  return 0


def populateNikeWomenTables():

  print('Adding NikeWomens Content to Database, please wait...')
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
    val =  (str(item['vendor']), str(item['gender']), title, str(item['brand']), retail, price, discount, str(item['image-link']), link)

    #print("NikeWomen item number "+str(count))
    cursor.execute(sql, val)
  conn.commit()

  # Removes Duplicate Rows
  cursor.execute("CREATE TABLE tempNW SELECT DISTINCT * FROM NikeWomenTemp;")
  cursor.execute("ALTER TABLE NikeWomenTemp RENAME junk;")
  cursor.execute("ALTER TABLE tempNW RENAME NikeWomenTemp;")
  cursor.execute("DROP TABLE junk;")

  # Drops old table
  cursor.execute("DROP TABLE IF EXISTS NikeWomen;")

  # Swaps in new table
  cursor.execute('ALTER TABLE NikeWomenTemp RENAME TO NikeWomen;')

  # Replaces old temp tables
  cursor.execute('CREATE TABLE NikeWomenTemp LIKE NikeWomen;')
  conn.commit()
  print("NikeWomens... Done!")
  return 0


if __name__=='__main__':

  selectBrandGender = sys.argv[1]

  if(selectBrandGender == "nrm"):
    populateNordstromRackMenTables()
  elif(selectBrandGender == "nrw"):
    populateNordstromRackWomenTables()
  elif(selectBrandGender == "nm"):
    populateNikeMenTables()
  else:
    populateNikeWomenTables()

  cursor.close()
  conn.close()
