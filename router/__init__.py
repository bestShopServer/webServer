
from config import common

class Route(object):
    """ 把每个URL与Handler的关系保存到一个元组中，然后追加到列表内，列表内包含了所有的Handler """

    def __init__(self):
        self.urls = list() # 路由列表

    def __call__(self, url=None, *args, **kwargs):
        def register(cls):

            urlnew = "/{}{}/{}/{}/{}".format(
                common.get("version", "v1"),
                common.get("api_base", "/api"),
                str(cls).split('.')[1],
                str(cls).split('.')[2],
                cls.__name__ if not url else url.replace('/',''),
            )
            self.urls.append((urlnew, cls)) # 把路由的对应关系表添加到路由列表中
            if kwargs.get("id",None):
                self.urls.append(("{}/{}".format(urlnew,"(.*)"), cls))
            return cls

        return register

route = Route()



