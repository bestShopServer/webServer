


import os
import sys
import django

if __name__ == "__main__":
    pathname = os.path.dirname(os.path.abspath(__file__))
    sys.path.insert(0, pathname)
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "utils.django.settings")

    django.setup()

    from utils import configinit_setup
    from utils import Server

    configinit_setup()
    Server().start()