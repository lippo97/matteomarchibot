from apscheduler.schedulers.blocking import BlockingScheduler
import logging

class MyBlockingScheduler(BlockingScheduler):

    def add_jobs(self, events):
        jobs = []
        for date, callback in events:
            j = self.add_job(callback, 'cron', month=date.month,
                             day=date.day, hour=date.hour, minute=date.minute,
                             second=date.second)
            jobs.append(j)
        logging.info('Scheduled tasks: {}'.format(jobs))
        return jobs

scheduler = MyBlockingScheduler({
    'apscheduler.timezone': 'Europe/Rome',
})
