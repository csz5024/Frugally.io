# script used to run the scrapy spiders

from crontab import CronTab

if __name__ == '__main__':
    cron = CronTab(user='frugally')
    job = cron.new(command="python updateNikeMen.py")
    job.hour.ever(12)

    cron.write()
