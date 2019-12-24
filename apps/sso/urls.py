from tornado.web import url
from apps.sso.api import *
from router import api_base_url,join_url

api_url = join_url(api_base_url,"/sso")

urlpattern = [
    url(join_url(api_url, '/logout'), logout),
    url(join_url(api_url,'/login'),login),
]