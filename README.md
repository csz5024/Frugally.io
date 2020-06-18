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
 1. [UNIX Basics for Navigating the Server over SSH](#UnixCommands)
 2. [Server Configurations](#ServerConfigurations)

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
  - **MySQL Login Command:** `/usr/bin/mysql -u root -p`
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
 

<a name="ServerConfigurations"/>

## Server Configurations

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

