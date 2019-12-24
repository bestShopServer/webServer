

api_base_url = "/api/v1"

def join_url(baseurl , url):
    return "{}{}".format(baseurl,url)


from .urls import urlpattern

