# Frugally.io
###### A Smarter Shopping Experience


## About our project
Frugally is a smarter online shopping experience. Minimize your time spent staring at a screen by having all of the best deals from all of your favorite vendors in one convenient place. Whats more, we have our own algorithms set in place to recommend you deals based upon your previous purchases. Create an account today to take full advantage!

Frugally is a simple design that employs the use of Selenium's web scraping libraries to gather all of the best deals from a set list of vendors. By handing this data off to our full stack web server (Hardware owned!), we are able to create a truly unique shopping experience that is curated to the user. All of your data is stored at home, right here in Philadelphia Pennsylvania- and in future iterations will be stored in the safest place of all; the Blockchain.

Frugally is an entirely free service to the user, however feel free to buy your favorite team of engineers and entrepreneurs a cup of coffee by donating to our site (insert link here). If you would like to get involved or have any suggestions, email us at frugally@frugally.io. 

> And then came that girl who rowed in the dark. Each night she paused to relay her coordinates, how her body was performing, and the atmospheric conditions. Often she noted things-the outlines of birds migrating at night, a whale shark seining for krill off her bow. She had, she said, a growing ability to dream while she rowed.
>
> *The Orphan Master's Son by Adam Johnson*

## Table of Contents


## Server Configurations

Frugally.io

Need to update SSL certificates every 60 days

iptables:
Need to edit on physical server restart
```
iptables-save > iptables.dump
iptables-restore < iptables.dump

iptables -I INPUT 1 blah blah blah
sudo iptables -A INPUT -p tcp -m multiport --dports 80,443 -m conntrack --ctstate NEW,ESTABLISHED -j ACCEPT
sudo iptables -A OUTPUT -p tcp -m multiport --dports 80,443 -m conntrack --ctstate ESTABLISHED -j ACCEPT
iptables -D INPUT 5
iptables -L
```

frugally.wsgi
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
  ServerName 192.168.1.xxx
  ServerAdmin caseyzduniak@gmail.com
  ErrorLog /var/www/Frugally/logs/error.log
  CustomLog /var/www/Frugally/logs/access.log combined
  
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
```

