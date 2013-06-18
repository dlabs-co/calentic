from apscheduler.scheduler import Scheduler
import calentic.scrappery

sched = Scheduler()

@sched.cron_schedule(day_of_week='mon-fri', hour=17)
def scheduled_job():
    scrappery.main()    

sched.start()

while True:
    pass
