# script used to run the scrapy spiders

from crontab import CronTab

if __name__ == '__main__':
    cron = CronTab(user='frugally')
    cron.remove_all()
    job = cron.new(command="python3 updateNikeMen.py")
    job.hour.every(12)
    job2 = cron.new(command="python3 updateNikeWomen.py")
    job2.hour.every(12)

    #job.every_reboot()
    #job2.every_reboot()

    for item in cron:
        print(item)
    print(job.is_valid())
    print(job2.is_valid())

    cron.write()
