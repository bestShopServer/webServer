
from web.sso import urls as sso_urls
from web.public import urls as public_urls
from web.user import urls as user_urls
from web.shop import urls as shop_urls
from web.goods import urls as goods_urls

urlpattern=[
    #
    # (r"/static/images/(.*)", StaticFileHandler, {"path":"/static/images/"})
]

urlpattern+=sso_urls.urlpattern
urlpattern+=public_urls.urlpattern
urlpattern+=user_urls.urlpattern
urlpattern+=shop_urls.urlpattern
urlpattern+=goods_urls.urlpattern