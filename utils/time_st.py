

import time

class MyTime(object):

    def __init__(self):
        pass

    @property
    def timestamp(self):
        return int(time.time())

    def today(self,format_v="%Y-%m-%d %H-%M-%S"):
        return time.strftime(format_v, time.localtime())

