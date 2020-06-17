import mysql.connector

conn = mysql.connector.connect(
  host="localhost",
  user="yourusername",
  password="yourpassword",
  database="mydatabase"
)

def populateTables():
  #conn = mysql.connect()
  cursor = conn.cursor()
  #cursor.execute('CREATE TABLE IF NOT EXISTS Nike(NAME CHAR(100), SEX CHAR(1), PRICE CHAR(10))')

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

      cursor.execute(sql, val)

  conn.commit()
  conn.close()
  return 0

if __name__=='__main__':
  populateTables()
