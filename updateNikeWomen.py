# update nike women

import os
import time
import subprocess

#finish this
if __name__ == '__main__':
    newlist = subprocess.Popen("sudo -S scrapy crawl NikeWomen -o NikeWomen0.json", 'w').write('Shoelas')
    #this is bad programming but oh well
    while newlist.poll() == None:
        time.sleep(1)
        continue
    os.popen("sudo -S rm NikeWomen.json", 'w').write('Shoelas')
    os.popen("sudo -S mv NikeWomen0.json NikeWomen.json", 'w').write('Shoelas')
