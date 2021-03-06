import time
import logging
from schedule import Scheduler

class BlockingScheduler(Scheduler):

    def run_blocking(self):
        try:
            while True:
                self.run_pending()
                time.sleep(1)
        except KeyboardInterrupt:
            logging.info('Leaving scheduler...')


scheduler = BlockingScheduler()
