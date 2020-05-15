# Frugally.io
Frugally.io

#####################################################

frugally.wsgi
```
#!/usr/bin/python3
import sys
import logging
logging.basicConfig(stream=sys.stderr)
sys.path.insert(0,"/var/www/Frugally/")

from Frugally import app as application
```
######################################################

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
######################################################
