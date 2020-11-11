
import json,traceback
from functools import wraps
from loguru import logger
from utils.exceptions import PubErrorCustom,InnerErrorCustom
from utils.http.response import HttpResponse
from utils.aes import decrypt,encrypt
from utils.database import MysqlPool
from apps.utlis import get_response_handler

from utils.decorator.utils import request_before_func_run,run_before_func_run

class Core_connector:

    def __init__(self,**kwargs):

        self.pk = None

        #是否加数据库事务
        self.isTransaction = kwargs.get('isTransaction',True)

        #是否校验ticket
        self.isTicket = kwargs.get('isTicket', True)

        #是否校验租户ID
        self.isMerchant = kwargs.get('isMerchant', False)

        #是否获取参数
        self.isParams = kwargs.get('isParams',True)

        #是否加密
        self.isPasswd = kwargs.get('isPasswd', False)

        #自动化处理参数
        """
            robot:
                form_class => Form校验类
                model_class => 模型集合
                    model_class => 关联表模型
                    is_father => 是否根部
                    data_pool => 对应数据
                        "self"=> self中的值
                        "custom"=> 自定义值
                        "instance" => 母表中的值
                        "last_ids_key" => 母(上级层级不限)表关联ID 字段
                        "last_ids_level" => 关联ID往上层级
                        "form"=>form中哪个值里取(其它所有值)
                    child => 关联子集
        """
        self.robot = kwargs.get("robot",None)

        #新增前置处理
        self.add_before_handler = kwargs.get("add_before_handler",None)

        #新增后置处理
        self.add_after_handler = kwargs.get("add_after_handler",None)

        #修改前置处理
        self.upd_before_handler = kwargs.get("upd_before_handler", None)

        #修改后置处理
        self.upd_after_handler = kwargs.get("upd_after_handler",None)

        #删除前置处理
        self.del_before_handler = kwargs.get("del_before_handler", None)

        #查询前置处理
        self.get_before_hander = kwargs.get("get_before_handler",None)

        #是否支持批量删除
        self.is_del_batch = kwargs.get("is_del_batch", True)

    async def __request_validate(self,outside_self,*args,**kwargs):

        await request_before_func_run(connector=self,connector_app=outside_self,args=args,kwargs=kwargs)

    async def __run_before_handler(self,outside_self,*args,**kwargs):

        return await run_before_func_run(connector=self,connector_app=outside_self,args=args,kwargs=kwargs)

    async def __run(self, func, outside_self, *args, **kwargs):

        if self.isTransaction:
            async with MysqlPool().get_conn.atomic_async():
                r = await self.__run_before_handler(outside_self,*args, **kwargs)
                res = await func(outside_self, *args, **kwargs)
        else:
            r = await self.__run_before_handler(outside_self, *args, **kwargs)
            res = await func(outside_self, *args, **kwargs)

        if r:
            res = r

        if not isinstance(res, dict):
            res = {'data': None, 'msg': None, 'header': None}
        if 'data' not in res:
            res['data'] = None
        if 'count' not in res:
            res['count'] = 0
        if 'msg' not in res:
            res['msg'] = {}
        if 'header' not in res:
            res['header'] = None

        logger.info("\n返回的数据: {}".format(json.dumps(res['data'],indent=4)))
        if self.isPasswd and res['data']:
            res['data'] = encrypt(json.dumps(res['data'])).decode('ascii')

        return HttpResponse(self=outside_self,data=res['data'], headers=res['header'], msg=res['msg'],count=res['count'])

    def __response__validate(self, outside_self, func):

        pass

    def __call__(self,func):
        @wraps(func)
        async def wrapper(outside_self,*args, **kwargs):
            try:
                await self.__request_validate(outside_self,*args,**kwargs)
                response = await self.__run(func,outside_self,*args, **kwargs)
                self.__response__validate(outside_self,func)

                await outside_self.finish(response)
            except PubErrorCustom as e:
                await outside_self.finish(HttpResponse(success=False, msg=e.msg, data=None))
                s = traceback.format_exc()
                logger.error(s)
            except InnerErrorCustom as e:
                await outside_self.finish(HttpResponse(success=False, msg=e.msg, data=None,rescode=e.code))
                s = traceback.format_exc()
                logger.error(s)
            except Exception as e:
                await outside_self.finish(HttpResponse(success=False, msg=str(e), data=None))
                s = traceback.format_exc()
                logger.error(s)

        return wrapper