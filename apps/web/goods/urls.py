from tornado.web import url
from apps.web.goods.api import *
from router import api_base_url,join_url

api_url = join_url(api_base_url,"/goods")

urlpattern = [
    url(join_url(api_url, '/goodscategorystyle'), goodscategorystyle),
    url(join_url(api_url, '/goodscategorystyle/(.*)'), goodscategorystyle),
    url(join_url(api_url, '/goodscategory'), goodscategory),
    url(join_url(api_url, '/goodscategory/(.*)'), goodscategory),
    url(join_url(api_url, '/goods'), goods),
    url(join_url(api_url, '/goods/(.*)'), goods),
    url(join_url(api_url, '/skugroup'), skugroup),
    url(join_url(api_url, '/skugroup/(.*)'), skugroup),
    url(join_url(api_url, '/skuspecvalue'), skuspecvalue),
    url(join_url(api_url, '/skuspecvalue/(.*)'), skuspecvalue),
]