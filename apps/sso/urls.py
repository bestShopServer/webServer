from tornado.web import url
from apps.sso.api import *

urlpattern = (
    # url("/test", TestHandler),
    url("/login",LoginHandler)
)