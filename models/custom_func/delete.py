

from functools import wraps

from utils.time_st import MyTime

class deleteCustom(object):

    async def before_hander(self):
        pass

    async def after_handler(self):
        pass

    def __call__(self,func):
        @wraps(func)
        async def wrapper(outside_self,obj, recursive=False, delete_nullable=False):

            await self.before_hander()
            response = await func(outside_self, obj, recursive, delete_nullable)

            return response

        return wrapper