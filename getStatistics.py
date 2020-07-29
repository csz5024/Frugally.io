import mysql.connector

# Data collected since July 28th
if __name__ == '__main__':
	conn = mysql.connector.connect(
		host="localhost",
		user="frugally",
		password="Shoelas20",
		database="BigDataDave"
	)
	cursor = conn.cursor()

        # All of the Users
	sql = "SELECT * FROM Users ORDER BY timezone"
        cursor.execute(sql)
	results = cursor.fetchall()

        # All of the Products Clicked
        sql = "SELECT * FROM ProductHistory ORDER BY price"
        cursor.execute(sql)
        results = cursor.fetchall()

	# Number of each vendor clicked, sales, average discount, total savings, and average savings per click
	sql = "SELECT DISTINCT vendor, SUM(clicked), SUM(clicked*price) as Sales, AVG(discount), SUM(retailprice-price) as TotalSavings, AVG(retailprice-price) as AvgSavingsPerClick FROM LinksClicked l RIGHT JOIN ProductHistory p ON l.link=p.link GROUP BY vendor ORDER BY Sales DESC;"

        # Number of each brand clicked, sales, average discount, total savings, and average savings per click
	sql = "SELECT DISTINCT brand, SUM(clicked), SUM(clicked*price) as Sales, AVG(discount) FROM LinksClicked l RIGHT JOIN ProductHistory p ON l.link=p.link GROUP BY brand ORDER BY Sales DESC;"

        # Total amount of sales
	sql = "SELECT DISTINCT SUM(clicked*price) as Total FROM LinksClicked l RIGHT JOIN ProductHistory p ON l.link=p.link;"

