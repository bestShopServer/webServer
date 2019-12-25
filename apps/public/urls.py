from tornado.web import url
from apps.public.api import *
from router import api_base_url,join_url

api_url = join_url(api_base_url,"/public")

urlpattern = [
    url(join_url(api_url, '/attachmentgroup'), attachmentgroup),
    url(join_url(api_url, '/attachmentgroup/([0-9]+)'), attachmentgroup),
    url(join_url(api_url, '/attachment'), attachment),
    url(join_url(api_url, '/attachment/([0-9]+)'), attachment)
]