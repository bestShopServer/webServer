

from apps.sso import urls as sso_urls
from apps.public import urls as public_urls
from apps.user import urls as user_urls

urlpattern=[
    #
    # (r"/static/images/(.*)", StaticFileHandler, {"path":"/static/images/"})
]

urlpattern+=sso_urls.urlpattern
urlpattern+=public_urls.urlpattern
urlpattern+=user_urls.urlpattern