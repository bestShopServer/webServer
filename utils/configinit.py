
import os
import sys

PROJECT_PATH = os.path.join(os.path.dirname(os.path.realpath(__file__)), os.path.pardir)
if PROJECT_PATH not in sys.path:
    sys.path.insert(0, PROJECT_PATH)

from tornado.options import define, options, Error
from config import config_insert

# options.logging = None


def setup():

    try:
        options.parse_command_line()
    except Error as e:
        print (e)
        sys.exit()

    for config_key in config_insert:
        for key in config_insert[config_key]:
            define(config_key +'_' +key ,default=config_insert[config_key][key])

    log_path =os.path.join(PROJECT_PATH ,'logs')
    if not os.path.exists(log_path):
        os.makedirs(log_path)

if __name__=='__main__':

    setup()
