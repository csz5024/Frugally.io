# Frugally.io
###### A Smarter Shopping Experience

https://frugally.io


## About our project
Frugally is a smarter online shopping experience. Minimize your time spent staring at a screen by having all of the best deals from all of your favorite vendors in one convenient place. Whats more, we have our own algorithms set in place to recommend you deals based upon your previous purchases. Create an account today to take full advantage!

Frugally is a simple design that employs the use of Selenium's web scraping libraries to gather all of the best deals from a set list of vendors. By handing this data off to our full stack web server (Hardware owned!), we are able to create a truly unique shopping experience that is curated to the user. All of your personal data is stored at home, right here in Philadelphia Pennsylvania- and in future iterations, will be stored in the safest place on earth; the Blockchain.

Frugally is an entirely free service to the user, however feel free to buy your favorite team of engineers and entrepreneurs a cup of coffee by donating to our site https://www.patreon.com/frugallyio?fan_landing=true. If you would like to get involved or have any suggestions, email us at frugally@frugally.io. 

> And then came that girl who rowed in the dark. Each night she paused to relay her coordinates, how her body was performing, and the atmospheric conditions. Often she noted things-the outlines of birds migrating at night, a whale shark seining for krill off her bow. She had, she said, a growing ability to dream while she rowed.
>
> *The Orphan Master's Son by Adam Johnson*

## Table of Contents
 1. [Frugally Web Server](#WebServer)
 2. [Frugally Database](#Database)
 3. [Scraping](#Scraping)
 4. [Server Configurations](#ServerConfigurations)
 5. [Porkbun Login Information](#Porkbun)
 6. [UNIX Basics for Navigating the Server over SSH](#UnixCommands)
 7. [Guide for Steve](#Guide)

<a name="WebServer"/>

## Frugally Web Server
This section details the code that can be found on the Github Repository, as well as under the `/var/www/Frugally/Frugally` directory on the server
### File Structure
```
Frugally/
├── PopulateDB.py
├── README.md
├── __init__.py
├── chromedriver.exe
├── flask.log
├── nordstromracksales/
│   ├── NikeMen.json
│   ├── NikeWomen.json
│   ├── NordstromRackMen.json
│   ├── NordstromRackWomen.json
│   ├── scrapy.cfg
│   └── nordstromracksales/
|       ├── items.py
|       ├── middlewares.py
|       ├── pipelines.py
|       ├── settings.py
|       ├── module/
|       │   ├── __init__.py
|       │   ├── items.py.tmpl
|       │   ├── middlewares.py.tmpl
|       │   ├── pipelines.py.tmpl
|       │   ├── settings.py.tmpl
|       │   └── spiders/
│       |       └── __init__.py 
|       └── spiders/
|           ├── __init__.py
|           ├── adidas_spider.py
|           ├── asos_spider.py
|           ├── newbalance_spider.py
|           ├── nike_spider_men.py
|           ├── nike_spider_women.py
|           ├── nordstromrack_spider.py
|           ├── nordstromrack_spider_men.py
|           ├── nordstromrack_spider_women.py
|           ├── patagonia_spider.py
│           └── urbanoutfitters_spider.py 
├── static/
│   ├── css/
|   │   ├── font-awesome.min.css
|   │   ├── skel.css
|   │   ├── style-mobile.css
|   │   ├── font-awesome.min.css
|   │   ├── skel.css
|   │   ├── style-mobile.css
|   │   ├── style-narrow.css
|   │   ├── style-narrower.css
|   │   ├── style-normal.css
|   │   ├── style-wide.css
|   │   └── style.css
│   ├── fonts/
|   │   ├── FontAwesome.otf
|   │   ├── fontawesome-webfont.eot
|   │   ├── fontawesome-webfont.svg
|   │   ├── fontawesome-webfont.ttf
|   │   └── fontawesome-webfont.woff
│   ├── images/
│   └── js/
|       ├── init.js
|       ├── jquery.droptron.min.js
|       ├── jquery.min.js
|       ├── skel-layers.min.js
|       └── skel.min.js
└── templates/
    ├── LICENSE.txt
    ├── google5e9dcfe4850ad995.html
    ├── index.html
    ├── login.html
    ├── mens.html
    ├── womens.html
    ├── 500.html
    ├── robots.txt
    ├── sitemap.xml
    └── template.html
```

<a name="Database"/>

## Frugally Database
This section details the MySQL Database used to hold all of our scraped product listings on the site
  - **MySQL Config:** `sudo nano /etc/mysql/mysql.conf.d/mysqld.cnf`
  - **MySQL Login Command:** `/usr/bin/mysql -u frugally -p`
  - **MySQL Data Directory Command:** `select @@datadir;` - Shows where the Databases are located
  - **MySQL Database Status Command:** `SHOW ENGINE INNODB STATUS\G`

<a name="Scraping"/>

## Scraping
This section details the web scraping.



<a name="ServerConfigurations"/>

## Server Configurations

list crontab configurations ```sudo crontab -e```
``` grep CRON /var/log/syslog```

Need to update SSL certificates every 60 days

This whole process is the biggest pain. be patient and methodical when configuring apache settings, debugging is limited.
make sure the development server is ready for production first, then place the whole thing ontop of apache to minimize the possible number of errors going forward. good luck.

frugally.wsgi (make sure you install wsgi for python3)
```
#!/usr/bin/python3
import sys
import logging
logging.basicConfig(stream=sys.stderr)
sys.path.insert(0,"/var/www/Frugally/")

from Frugally import app as application
```


/etc/apache2/sites-available/Frugally.conf
```
<VirtualHost *:80>
  #ServerName 192.168.1.235
  ServerName frugally.io
  ServerAdmin caseyzduniak@gmail.com

  ErrorLog /var/www/Frugally/logs/error.log
  CustomLog /var/www/Frugally/logs/access.log combined
  LogLevel info

  WSGIDaemonProcess frugally user=www-data group=www-data threads=5
  WSGIProcessGroup frugally
  WSGIScriptAlias / /var/www/Frugally/frugally.wsgi
  <Directory /var/www/Frugally/Frugally/>
    Options Indexes FollowSymLinks
    AllowOverride None
    Require all granted
  </Directory>

  Alias /static /var/www/Frugally/Frugally/static
  <Directory /var/www/Frugally/Frugally/static/>
    Require all granted
  </Directory>
</VirtualHost>

<VirtualHost *:443>
  #ServerName 192.168.1.235
  ServerName frugally.io
  ServerAdmin caseyzduniak@gmail.com

  ErrorLog /var/www/Frugally/logs/ssl_error.log
  CustomLog /var/www/Frugally/logs/ssl_access.log combined
  LogLevel info

  SSLEngine on
  SSLCertificateFile /var/www/Frugally/frugally.io-ssl-bundle/domain.cert.pem
  SSLCertificateKeyFile /var/www/Frugally/frugally.io-ssl-bundle/private.key.pem
  SSLCertificateChainFile /var/www/Frugally/frugally.io-ssl-bundle/intermediate.$

  WSGIProcessGroup frugally
  WSGIScriptAlias / /var/www/Frugally/frugally.wsgi
  <Directory /var/www/Frugally/Frugally/>
    Options Indexes FollowSymLinks
    AllowOverride None
    Require all granted
  </Directory>

  Alias /static /var/www/Frugally/Frugally/static
  <Directory /var/www/Frugally/Frugally/static/>
    Require all granted
  </Directory>
</VirtualHost>

```


<a name="Porkbun"/>

## Porkbun
Login: jadblaik
pw: tJgxbMgsdG@!!M%P5n6s

<a name="UnixCommands"/>

## Unix Commands
This section lists a few essential unix commands needed for navigating through the Frugally Server
### Restarting the Physical Server
**WARNING** This command will restart the physical hardware server, so make sure you save any work and that you know what you are doing when you run this command. You will lose SSH connection upon execution, and will have to wait a few minutes before it fully boots back up.

`sudo restart`
### Resetting iptables
For some reason, when the server undergoes a hard restart, the firewall of the physical server resets. Below are the necessary commands to get back up and running. Don't mess with this unless you know what you are doing.
```
iptables-save > iptables.dump
iptables-restore < iptables.dump

iptables -L
iptables -D INPUT <index of the REJECT rule to delete.>
sudo iptables -A INPUT -p tcp -m multiport --dports 80,443 -m conntrack --ctstate NEW,ESTABLISHED -j ACCEPT
sudo iptables -A OUTPUT -p tcp -m multiport --dports 80,443 -m conntrack --ctstate ESTABLISHED -j ACCEPT
```

### Restarting Software Components
`sudo systemctl restart <component name>`
 - `apache2`: restarts the web server
 - `mysql`: restarts the database
 - You can also swap `restart` for `start` `stop` or `status`
 
 ### Important Directory Locations
  - **Git Directory:** `/var/www/Frugally/Frugally` - One directory up are configuration files related to the backend components, and generally should not be touched.
  - **Flask Logs:** `/var/www/Frugally/Frugally/flask.log`
  - **Apache Logs:** `/var/www/Frugally/logs`
  - **WSGI Config:** `/var/www/Frugally/frugally.wsgi`
  - **Apacahe Config:** `/etc/apache2/sites-available/Frugally.conf`
  - **MySQL Config:** `sudo nano /etc/mysql/mysql.conf.d/mysqld.cnf`
  - **MySQL Login Command:** `/usr/bin/mysql -u frugally -p`
  - **MySQL Data Directory Command:** `select @@datadir;` - Shows where the Databases are located
  
  ### Useful Commands
   - `cd <directory>` - change directory
   - `pwd` - shows the present working directory
   - `dir` - shows the contents of the current directory
   - `df` - shows disk space on the root, disk1 and disk2
   - `nano <filename>` - text editor
   - `cp <source> <destination>` - copy file
   - `rm <filename>` - delete file
   - `mv <source> <destination>` - move or rename file
   
   ### Useful Git Commands
   - `sudo git pull` - downloads the latest code from the master branch
   - `sudo git add .` - add all files to be staged for commit
   - `git status` - show the status of the git directory
   - `sudo git commit -am "message content"` - commit a change to be made to the git directory
   - `sudo git push origin <branch name>` - push the commit up to github branch name

<a name="Guide"/>

## Guide for Steve
### Debugging process
1. Log on to the server
2. change directory ```cd /var/www/Frugally/Frugally```
3. view contents of directory ```dir```
4. open the DBqueries.py file ```sudo nano DBqueries.py```
5. make edits to ```getSQL``` functions
6. save and exit by pressing ```ctrl+x``` or just save ```ctrl+s```
7. restart the server to test your changes ```sudo systemctl restart apache2```
8. navigate to the website
9. If you get an error page:
   - check the frugally error logs ```sudo nano flask.log``` and scroll to the bottom. This should give you a standard python error.
   - be sure to delete the file afterwards to reset it ```sudo rm flask.log```
   - check the apache error logs: 
     - first go up one directory ```cd ..```
     - then change directories ```cd logs``` view the contents of the directory ```dir```
     - check the ```error.log``` file as well as the ```ssl_error.log``` by typing ```sudo nano error.log``` and scrolling to the bottom.
     - feel free to delete these files afterwards as well.
     
If you find that still, after all of that, you dont have a clue as to why your code isnt working, this is completley common. I have banged my head on my desk trying to get the stupid error logs to work, and they still dont log some errors. Just try to think it through.

### Additional super useful debugging tip
- place ```app.logger.info("<enter debugging message here>")``` anywhere in the __init__.py file or DBqueries.py to print information to the flask.log file. If all else fails, this can end up being your guardian angel.

best of luck and godspeed.

### First Assignment:
- Create SQL Statements that filter content based on user input.

In DBqueries.py you will find the ```getSQLdiscount``` function. This function will return an array of products, sorted from best discount to lowest discount, with any combination of filters applied.

the filters parameter should look something like ```[[gender, m/f], [vendor, [nike, nordstrom]], [brand, [burberry, guess, zara ...]]]```
unpack the filters and insert them into the corresponding SQL statements so that the database returns the correct set of products. You should have multiple SQL statements, one for each table (in other words one for each vendor). To collect the results, just append the item variable by ```item = item + cursor.fetchall()``` after each SQL statement. then at the very end, return item.

```
# The goal of this function is to return a set of products
# whose attributes match that of the filters
# and are sorted in order of highest discount to lowest
def getSQLdiscount(filters):

    # Parse out the filters
    if(filters!=None):
        gender = str(filters[0][1]).lower()
        filtervendor = filters[1][1]
        filterbrands = filters[2][1]
    else:
        gender = "all"
        filtervendor = "all"
        filterbrands = "all"

    cursor = conn.cursor()
    cursor.execute('SELECT * FROM NordstromRackMen WHERE', gender)

    item = cursor.fetchall()

```

once again the login for mysql is ```/usr/bin/mysql -u frugally -p``` then just enter the super secret password.

If you want to test your query before putting it in the DBqueries.py file (which I would recommend) 

1. login to the mysql server ```/usr/bin/mysql -u frugally -p```
2. ```use Frugally```
3. ```show tables;``` and ```describe [tablename];```
4. write the sql statements here and see what kind of output you get 
   - Ex. ```SELECT * FROM NordstromRackMen WHERE gender='male', brand='burberry' OR brand='guess' OR brand='zara' ORDER BY discount;```


Machine Learning link: https://amulyayadav.github.io/DS442/
