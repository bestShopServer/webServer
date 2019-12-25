
from apps.base import BaseHandler
from utils.decorator.connector import Core_connector
from utils.exceptions import PubErrorCustom
from models.public import AttachMentGroup,AttachMent
from playhouse.shortcuts import model_to_dict
# from peewee import JOIN

class attachmentgroup(BaseHandler):

    """
    素材分组
    """

    @Core_connector()
    async def post(self):

        if not self.data.get("name",None):
            raise PubErrorCustom("名称是空!")

        if not self.data.get("type",None):
            raise PubErrorCustom("类型时空!")

        await self.db.create(
            AttachMentGroup,
            name=self.data.get("name"),
            type=self.data.get("type"),
            userid=self.user.get("userid"))

        # res = model_to_dict(group)

        return None

    @Core_connector()
    async def put(self,pk=None):

        try:
            group = await self.db.get(AttachMentGroup,id=pk,userid=self.user['userid'])
        except AttachMentGroup.DoesNotExist:
            raise PubErrorCustom("拒绝访问!")

        group.name = self.data['name']
        await self.db.update(group)

        return None

    @Core_connector()
    async def delete(self,pk=None):

        try:
            group = await self.db.get(AttachMentGroup,id=pk,userid=self.user['userid'])
        except AttachMentGroup.DoesNotExist:
            raise PubErrorCustom("拒绝访问!")

        await self.db.delete(group)

        return None

    @Core_connector(isTransaction=False)
    async def get(self, pk=None):

        # try:
        #     res = await self.db.get(AttachMentGroup,id=pk,userid=self.user['userid'])
        # except AttachMentGroup.DoesNotExist:
        #     raise PubErrorCustom("拒绝访问!")

        query = AttachMentGroup.select()

        if pk:
            query = query.where(AttachMentGroup.id==pk)

        if self.data.get('type',None):
            query = query.where(AttachMentGroup.type == self.data.get('type'))

        query = query.where(AttachMentGroup.userid == self.user['userid']).order_by(AttachMentGroup.updtime.desc())


        # query = AttachMentGroup.select(AttachMentGroup,AttachMent).\
        #     join(AttachMent,join_type=JOIN.LEFT_OUTER,on=(AttachMent.grouid==AttachMentGroup.id))
        #
        # if pk:
        #     query.where(AttachMentGroup.id==pk)
        #
        # query.where(AttachMentGroup.userid==self.user['userid'],AttachMent.userid==self.user['userid'])
        #
        # data=[]
        # for item in await self.db.execute(query):
        #     attachmentgroup = model_to_dict(item)
        #     try:
        #         attachmentgroup['attachment'] = model_to_dict(item.attachment)
        #     except AttributeError:
        #         attachmentgroup['attachment'] = []
        #     data.append(attachmentgroup)
        data = [model_to_dict(item) for item in await self.db.execute(query)]
        if pk:
            data = data[0] if len(data) else {}

        return {"data":data }

class attachment(BaseHandler):

    """
    素材
    """

    @Core_connector()
    async def post(self):

        if not self.data.get("name",None):
            raise PubErrorCustom("名称是空!")

        if not self.data.get("url",None):
            raise PubErrorCustom("链接是空!")

        if not self.data.get("grouid",None):
            raise PubErrorCustom("组ID是空!")

        try:
            await self.db.get(AttachMentGroup,id=self.data.get("grouid"),userid=self.user['userid'])
        except AttachMentGroup.DoesNotExist:
            raise PubErrorCustom("拒绝访问!")

        await self.db.create(
            AttachMent,
            name=self.data.get("name"),
            url=self.data.get("url"),
            grouid=self.data.get("grouid"))

        return None

    @Core_connector()
    async def put(self,pk=None):

        try:
            obj = await self.db.get(AttachMent,id=pk,userid=self.user['userid'])
        except AttachMent.DoesNotExist:
            raise PubErrorCustom("拒绝访问!")

        try:
            await self.db.get(AttachMentGroup,id=self.data.get("grouid"),userid=self.user['userid'])
        except AttachMentGroup.DoesNotExist:
            raise PubErrorCustom("拒绝访问!")

        obj.name = self.data['name']
        obj.url = self.data['url']
        obj.grouid = self.data['grouid']

        await self.db.update(obj)

        return None

    @Core_connector()
    async def delete(self,pk=None):

        try:
            obj = await self.db.get(AttachMent,id=pk,userid=self.user['userid'])
        except AttachMent.DoesNotExist:
            raise PubErrorCustom("拒绝访问!")

        await self.db.delete(obj)

        return None

    @Core_connector(isTransaction=False)
    async def get(self, pk=None):

        query = AttachMent.select()

        if pk:
            query = query.where(AttachMent.id == pk)

        if self.data.get('grouid', None):
            query = query.where(AttachMent.grouid == self.data.get('grouid'))

        query = query.where(AttachMent.userid == self.user['userid']).order_by(AttachMent.updtime.desc())

        data = [model_to_dict(item) for item in await self.db.execute(query)]
        if pk:
            data = data[0] if len(data) else {}

        return {"data": data}