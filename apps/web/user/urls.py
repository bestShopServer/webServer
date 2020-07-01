from tornado.web import url
from apps.web.user.api import *
from router import api_base_url,join_url

api_url = join_url(api_base_url,"/user")

urlpattern = [
    url(join_url(api_url, '/userinfo'), userinfo),
]