import os
import time
import subprocess

#finish this
if __name__ == '__main__':
    newlist = subprocess.Popen("sudo -S scrapy crawl NikeMen -o NikeMen0.json", 'w').write('Shoelas')
    #this is bad programming but oh well
    #loops until the newlist process finishes
    while newlist.poll() == None:
        time.sleep(5)
        continue
    os.popen("sudo -S rm NikeMen.json", 'w').write('Shoelas')
    os.popen("sudo -S mv NikeMen0.json NikeMen.json", 'w').write('Shoelas')
