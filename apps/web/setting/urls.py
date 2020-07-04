from tornado.web import url
from apps.web.setting.api import *
from router import api_base_url,join_url

api_url = join_url(api_base_url,"/setting")

urlpattern = [
    url(join_url(api_url, '/farerule'), farerule),
    url(join_url(api_url, '/farerule/(.*)'), farerule),
]