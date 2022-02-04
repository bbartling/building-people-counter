import threading
import time
import schedule
from schedule import every, repeat

def job(name):
    print("I'm running on thread %s" % threading.current_thread())
    print('Hello', name)

def run_threaded(job_func):
    job_thread = threading.Thread(target=job_func)
    job_thread.start()

schedule.every(10).seconds.do(run_threaded, name='Alice')
schedule.every(10).seconds.do(run_threaded, name='Sam')
schedule.every(10).seconds.do(run_threaded, name='Bob')
schedule.every(10).seconds.do(run_threaded, name='Steve')
schedule.every(10).seconds.do(run_threaded, name='Lester')




while 1:
    schedule.run_pending()
    time.sleep(1)
