

from functools import wraps

from utils.time_st import MyTime

class createCustom(object):

    # def __init__(self,**kwargs):
    #     self.className = kwargs.get("className")

    async def before_hander(self,model_,data):
        data['createtime'] = MyTime().timestamp
        data['updtime'] = MyTime().timestamp

    async def after_handler(self):
        pass

    def __call__(self,func):
        @wraps(func)
        async def wrapper(outside_self,model_, **data):

            await self.before_hander(model_,data)

            response = await func(outside_self, model_, **data)

            return response

        return wrapper