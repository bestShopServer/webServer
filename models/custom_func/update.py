

from functools import wraps

from utils.time_st import MyTime

class updateCustom(object):

    async def before_hander(self,obj):

        obj.updtime = MyTime().timestamp

    async def after_handler(self):
        pass

    def __call__(self,func):
        @wraps(func)
        async def wrapper(outside_self,obj, only=None):

            await self.before_hander(obj)
            response = await func(outside_self, obj, only)

            return response

        return wrapper