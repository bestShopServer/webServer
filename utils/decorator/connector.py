
import json
from functools import wraps
from loguru import logger

from utils.exceptions import PubErrorCustom
from utils.http.response import HttpResponse
from utils.aes import decrypt,encrypt

class Core_connector:

    def __init__(self,**kwargs):
        #是否加密
        self.isPasswd = kwargs.get('isPasswd', False)

    def __request_validate(self,outside_self,**kwargs):

        if outside_self.request.method == 'POST':
            outside_self.data = outside_self.get_body_argument("data",None)
            if not outside_self.data:
                outside_self.data = json.loads(outside_self.request.body.decode('utf-8')).get("data",None)
        elif outside_self.request.method == 'GET':
            outside_self.data = outside_self.get_argument("data",None)

        if not outside_self.data:
            raise PubErrorCustom("拒绝访问!")

        if self.isPasswd:
            outside_self.data = json.loads(decrypt(outside_self.data))
        else:
            outside_self.data = json.loads(outside_self.data)

    async def __run(self, func, outside_self, *args, **kwargs):
        res = await func(outside_self, *args, **kwargs)

        if not isinstance(res, dict):
            res = {'data': None, 'msg': None, 'header': None}
        if 'data' not in res:
            res['data'] = None
        if 'msg' not in res:
            res['msg'] = {}
        if 'header' not in res:
            res['header'] = None

        print(res['data'])
        if self.isPasswd and res['data']:
            res['data'] = encrypt(json.dumps(res['data'])).decode('ascii')

        print(res['data'])

        return HttpResponse(self=outside_self,data=res['data'], headers=res['header'], msg=res['msg'])

    def __response__validate(self, outside_self, func):

        pass

    def __call__(self,func):
        @wraps(func)
        async def wrapper(outside_self,*args, **kwargs):
            try:
                self.__request_validate(outside_self,**kwargs)
                response = await self.__run(func,outside_self,*args, **kwargs)
                self.__response__validate(outside_self,func)

                outside_self.finish(response)
            except PubErrorCustom as e:
                outside_self.finish(HttpResponse(success=False, msg=e.msg, data=None))
                logger.warning(e.msg)
            except Exception as e:
                outside_self.finish(HttpResponse(success=False, msg=str(e), data=None))
                logger.exception("err")

        return wrapper