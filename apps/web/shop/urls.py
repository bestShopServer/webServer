from tornado.web import url
from apps.web.shop.api import *
from router import api_base_url,join_url

api_url = join_url(api_base_url,"/shop")

urlpattern = [
    url(join_url(api_url, '/baseinfo'), baseinfo),
    url(join_url(api_url, '/shoppage'), shoppage),
    url(join_url(api_url, '/shoppage/(.*)'), shoppage),
    url(join_url(api_url, '/shopconfig'), shopconfig),
    url(join_url(api_url, '/shopconfig/(.*)'), shopconfig)
]