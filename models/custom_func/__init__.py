


from peewee_async import Manager
from utils.time_st import MyTime

from models.custom_func.create import createCustom
from models.custom_func.update import updateCustom
from models.custom_func.delete import deleteCustom

class ManagerSon(Manager):

    @createCustom()
    async def create(self, model_, **data):
        return await super(ManagerSon, self).create(model_, **data)

    @updateCustom()
    async def update(self, obj, only=None):
        return await super(ManagerSon, self).update(obj,only)

    @deleteCustom()
    async def delete(self, obj, recursive=False, delete_nullable=False):
        return await super(ManagerSon, self).delete(obj,recursive,delete_nullable)