
import json,traceback
from functools import wraps
from loguru import logger
from utils.exceptions import PubErrorCustom,InnerErrorCustom
from utils.http.response import HttpResponse
from utils.aes import decrypt,encrypt
from utils.database import MysqlPool
from apps.utlis import get_response_handler

# import tornado.httputil.HttPHeaders

class Core_connector:

    def __init__(self,**kwargs):

        self.pk = None

        #是否加数据库事务
        self.isTransaction = kwargs.get('isTransaction',True)

        #是否加密
        self.isPasswd = kwargs.get('isPasswd', False)

        #是否校验ticket
        self.isTicket = kwargs.get('isTicket', True)

        #是否获取参数
        self.isParams = kwargs.get('isParams',True)


        #form校验
        self.form_class = kwargs.get("form_class",None)

        self.model_class = kwargs.get("model_class",None)

        self.pk_key = kwargs.get("pk_key",None)

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

        #是否支持批量删除
        self.is_del_batch = kwargs.get("is_del_batch", True)

        #是否常规查询
        self.is_query_standard = kwargs.get("is_query_standard", True)

    async def __request_validate(self,outside_self,*args,**kwargs):
        logger.info("\n请求IP：{}\n请求方法：{}".format(
            outside_self.request.remote_ip,
            outside_self.request.uri,
        ))
        #校验凭证并获取用户数据
        if self.isTicket:
            token = outside_self.request.headers.get_list("Authorization")
            if len(token)<=0:
                raise InnerErrorCustom(code="20001", msg="拒绝访问!")
            else:
                token = token[0]
            c = outside_self.redisC(key=token)
            result = await c.get_dict()
            if not result:
                raise InnerErrorCustom(code="20002",msg="拒绝访问")

            if result.get("status") == '1':
                raise PubErrorCustom("账户已到期!")
            elif result.get("status") == '2':
                raise PubErrorCustom("账户已冻结!")
            outside_self.user = result
            outside_self.token = token

        outside_self.data = None

        if self.isParams:
            if outside_self.request.method in ['POST','PUT','DELETE']:
                outside_self.data = outside_self.get_body_argument("data",None)
                if not outside_self.data:
                    outside_self.data = json.dumps(json.loads(outside_self.request.body.decode('utf-8')).get("data",None)) if outside_self.request.body \
                        else '{}'
                if not outside_self.data:
                    outside_self.data='{}'

                if self.is_query_standard:
                    self.is_query_standard = False
            elif outside_self.request.method == 'GET':
                outside_self.data = outside_self.get_query_argument("data",None)
            else:
                raise PubErrorCustom("拒绝访问!")

            if not outside_self.data:
                raise PubErrorCustom("拒绝访问!")

            if self.isPasswd:
                if outside_self.data != '{}':
                    outside_self.data = json.loads(decrypt(outside_self.data))
                else:
                    outside_self.data = json.loads(outside_self.data)
            else:
                outside_self.data = json.loads(outside_self.data)

            if outside_self.request.method == 'GET':
                if outside_self.data.get("page"):
                    outside_self.data['page'] = int(outside_self.data.get("page"))
                else:
                    outside_self.data['page'] = 1

                if outside_self.data.get("size"):
                    outside_self.data['size'] = int(outside_self.data.get("size"))
                else:
                    outside_self.data['size'] = 10

        logger.info("\n请求的数据: {}".format(outside_self.data))

    async def __run_before_handler(self,outside_self,*args,**kwargs):

        if len(args) and args[0]:
            self.pk = args[0]

        if self.form_class:

            if hasattr(outside_self, "user") and outside_self.data:
                outside_self.data['userid'] = outside_self.user['userid']
            if self.pk:
                outside_self.data[self.pk_key] = self.pk
            form_obj = self.form_class(**outside_self.data)

            if not form_obj.validate():
                error_str = ""
                for field in form_obj.errors:
                    error_str += "{}; ".format(form_obj.errors[field][0])
                raise PubErrorCustom(error_str)

            if outside_self.request.method == 'POST':
                data= form_obj.data
                if self.add_before_handler:
                    data = await self.add_before_handler(outside_self,data)

                kwargs['instance'] = await outside_self.db.create(self.model_class, **data)

                if self.add_after_handler:
                    kwargs['instance'] = await self.add_after_handler(outside_self, data,kwargs['instance'])

            elif outside_self.request.method == 'PUT':
                data=form_obj.data
                if not outside_self.data[self.pk_key]:
                    raise PubErrorCustom("pk not found!")
                if self.upd_before_handler:
                    data = await self.upd_before_handler(outside_self,data)
                d = self.model_class(**data)
                await outside_self.db.update(d)
                kwargs['instance'] = d

                if self.upd_after_handler:
                    kwargs['instance'] = await self.upd_after_handler(outside_self, data,kwargs['instance'])
        else:

            if outside_self.request.method == 'DELETE':

                if not self.pk and not outside_self.data.get("ids"):
                    raise PubErrorCustom("请选择数据!")

                if self.del_before_handler:
                    await self.del_before_handler(outside_self,self.pk if self.pk else outside_self.data.get("ids"))

                if self.pk:
                    try:
                        kwargs['instance'] = await outside_self.db.get(self.model_class, **{
                            self.pk_key: self.pk
                        })
                        await outside_self.db.delete(kwargs['instance'])
                    except self.model_class.DoesNotExist:
                        raise PubErrorCustom("无此记录!")
                else:

                    if not self.is_del_batch:
                        raise PubErrorCustom("此接口不支持批量删除!")

                    if not isinstance(outside_self.data.get("ids"),list):
                        raise PubErrorCustom("批量删除数据格式有误!")
                    delHandler = self.model_class.delete().where(getattr(self.model_class,self.pk_key) << outside_self.data.get("ids"))
                    await outside_self.db.execute(delHandler)
        return kwargs

    async def __run(self, func, outside_self, *args, **kwargs):

        if self.isTransaction:
            async with MysqlPool().get_conn.atomic_async():
                kwargs = await self.__run_before_handler(outside_self,*args, **kwargs)
                res = await func(outside_self, *args, **kwargs)
        else:
            kwargs = await self.__run_before_handler(outside_self, *args, **kwargs)
            res = await func(outside_self, *args, **kwargs)

        if self.is_query_standard:
            res['data'] = get_response_handler(self.pk,res['data'])

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

        logger.info("\n返回的数据: {}".format(res['data']))
        if self.isPasswd and res['data']:
            res['data'] = encrypt(json.dumps(res['data'])).decode('ascii')

        # if 'caches' in res and res['caches']:
        #     c = outside_self.redisC(key=None)
        #     for item in res['caches']:
        #         c.key = item['table']
        #         if item['method'] == 'save':
        #             await c.save(**item)
        #         elif item['method'] == 'delete':
        #             await c.delete(**item)
        #         elif item['method'] == 'save_ex':
        #             await c.save_ex(**item)

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

                outside_self.finish(response)
            except PubErrorCustom as e:
                outside_self.finish(HttpResponse(success=False, msg=e.msg, data=None))
                s = traceback.format_exc()
                logger.error(s)
            except InnerErrorCustom as e:
                outside_self.finish(HttpResponse(success=False, msg=e.msg, data=None,rescode=e.code))
                s = traceback.format_exc()
                logger.error(s)
            except Exception as e:
                outside_self.finish(HttpResponse(success=False, msg=str(e), data=None))
                s = traceback.format_exc()
                logger.error(s)

        return wrapper