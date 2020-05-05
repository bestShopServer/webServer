from tornado.web import url
from apps.goods.api import *
from router import api_base_url,join_url

api_url = join_url(api_base_url,"/goods")

urlpattern = [
    url(join_url(api_url, '/goodscategory'), goodscategory),
    url(join_url(api_url, '/goodscategory/(.*)'), goodscategory),
    url(join_url(api_url, '/goods'), goods),
    url(join_url(api_url, '/goods/(.*)'), goods),
    url(join_url(api_url, '/skugroup'), skugroup),
    url(join_url(api_url, '/skugroup/(.*)'), skugroup),
    url(join_url(api_url, '/sku'), sku),
    url(join_url(api_url, '/sku/(.*)'), sku),
]