import sched
import time


def print_time(a='default'):
    print("From print_time", time.ctime(), a)

s = sched.scheduler(time.ctime(), time.sleep)

#def simple():
#    print("10")

#s.enterabs(time.ctime(),1,print("10"))