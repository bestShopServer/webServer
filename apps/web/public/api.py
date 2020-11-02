
import os,aiofiles,uuid

from utils.decorator.connector import Core_connector
from utils.exceptions import PubErrorCustom

from models.public import AttachMentGroup,AttachMent

from apps.base import BaseHandler

from data.base import datacity

from apps.web.public.rule import AttachMentGroupRules,AttachMentRules,MenuRules
from router import route

@route()
class file(BaseHandler):
    """
    文件上传
    """
    @Core_connector(isParams=False)
    async def post(self):
        files = self.request.files.get("filename", None)
        if files:
            for file in files:
                new_file = "{}_{}".format(uuid.uuid4().hex,file['filename'])

                file_path =os.path.join(self.settings['images'], new_file)
                async with aiofiles.open(file_path, 'wb') as f:
                    await f.write(file['body'])

                return {"data":{"path":"{}/static/images/{}".format(self.settings['serverurl'],new_file)}}

        else:
            raise PubErrorCustom("文件上传失败!")

@route(None,id=True)
class attachmentgroup(BaseHandler):

    """
    素材分组
    """

    async def del_before_handler(self,**kwargs):

        pk = kwargs.get("pk")

        if isinstance(pk,list):
            for item in await self.db.execute(AttachMent.select().where(AttachMent.grouid << pk)):
                item.grouid = 0
                await self.db.update(item)
        else:
            for item in await self.db.execute(AttachMent.select().where(AttachMent.grouid == pk)):
                item.grouid = 0
                await self.db.update(item)

    @Core_connector(**AttachMentGroupRules.post())
    async def post(self,*args,**kwargs):
        pass

    @Core_connector(**AttachMentGroupRules.put())
    async def put(self,*args,**kwargs):
        pass

    @Core_connector(**{**AttachMentGroupRules.delete(),**{"del_before_handler":del_before_handler}})
    async def delete(self,*args,**kwargs):
        pass

    @Core_connector(**AttachMentGroupRules.get())
    async def get(self, pk=None,**kwargs):
        pass

@route(None,id=True)
class attachmentgroupbatch(BaseHandler):

    @Core_connector()
    async def post(self,*args,**kwargs):

        grouid = self.data.get("grouid",0)
        ids = self.data.get("ids",[])

        if not len(ids):
            raise PubErrorCustom("请选择素材!")

        if grouid!=0:
            try:
                await self.db.get(AttachMentGroup,merchant_id=self.user.merchant_id,id=grouid)
            except AttachMentGroup.DoesNotExist:
                raise PubErrorCustom("无此分组!")

        for item in await self.db.execute( AttachMent.select().where( AttachMent.id << ids)):
            item.grouid = grouid
            await self.db.update(item)

@route(None,id=True)
class attachment(BaseHandler):

    """
    素材
    """

    @Core_connector(**AttachMentRules.post())
    async def post(self,*args,**kwargs):
        pass

    @Core_connector(**AttachMentRules.put())
    async def put(self,*args,**kwargs):
        pass

    @Core_connector(**AttachMentRules.delete())
    async def delete(self,*args,**kwargs):
        pass

    @Core_connector(**AttachMentRules.get())
    async def get(self, pk=None):
        pass

@route(None,id=True)
class menu(BaseHandler):

    """
    菜单管理
    """

    @Core_connector(**MenuRules.post())
    async def post(self,*args,**kwargs):
        pass

    @Core_connector(**MenuRules.put())
    async def put(self,*args,**kwargs):
        pass

    @Core_connector(**MenuRules.delete())
    async def delete(self,*args,**kwargs):
        pass

    @Core_connector(**MenuRules.get())
    async def get(self, pk=None):
        pass

@route(None,id=True)
class citycode(BaseHandler):
    @Core_connector(isTransaction=False,is_query_standard=False)
    async def get(self, pk=None):
        return {"data": await datacity(redis=self.redis).get()}