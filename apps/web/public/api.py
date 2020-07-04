
import os,aiofiles,uuid
from loguru import logger

from utils.decorator.connector import Core_connector
from utils.exceptions import PubErrorCustom

from models.public import AttachMentGroup,AttachMent

from apps.base import BaseHandler

from apps.web.public.forms import AttachMentGroupForm,AttachMentForm

from apps.web.public.serializers import AttachMentGroupSerializer,AttachMentSerializer

from data.base import datacity

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


class attachmentgroup(BaseHandler):

    """
    素材分组
    """

    async def del_before_handler(self,pk):

        if isinstance(pk,list):
            for item in await self.db.execute(AttachMent.select().where(AttachMent.grouid << pk)):
                item.grouid = 0
                self.db.update(item)
        else:
            for item in await self.db.execute(AttachMent.select().where(AttachMent.grouid == pk)):
                item.grouid = 0
                self.db.update(item)

    @Core_connector(form_class=AttachMentGroupForm,model_class=AttachMentGroup,pk_key="id")
    async def post(self,*args,**kwargs):
        pass

    @Core_connector(form_class=AttachMentGroupForm,model_class=AttachMentGroup,pk_key="id")
    async def put(self,*args,**kwargs):
        pass

    @Core_connector(
        model_class=AttachMentGroup,
        pk_key="id",
        del_before_handler=del_before_handler)
    async def delete(self,*args,**kwargs):
        pass

    @Core_connector(isTransaction=False)
    async def get(self, pk=None,**kwargs):

        # query = AttachMentGroup.select().paginate(self.data['page'],self.data['size']).for_update()
        query = AttachMentGroup.select()

        if pk:
            query = query.where(AttachMentGroup.id==pk)

        if self.data.get('type',None):
            query = query.where(AttachMentGroup.type == self.data.get('type'))

        query = query.where(AttachMentGroup.userid == self.user['userid']).order_by(AttachMentGroup.createtime.desc())

        count = len(await self.db.execute(query))

        query = query.paginate(self.data['page'],self.data['size'])

        return {
            "data": AttachMentGroupSerializer(await self.db.execute(query),many=True).data,
            "count":count
        }

class attachmentgroupbatch(BaseHandler):

    @Core_connector()
    async def post(self,*args,**kwargs):

        grouid = self.data.get("grouid",0)
        ids = self.data.get("ids",[])

        if not len(ids):
            raise PubErrorCustom("请选择素材!")

        if grouid!=0:
            try:
                await self.db.get(AttachMentGroup,userid=self.user['userid'],id=grouid)
            except AttachMentGroup.DoesNotExist:
                raise PubErrorCustom("无此分组!")

        for item in await self.db.execute( AttachMent.select().where( AttachMent.id << ids)):
            item.grouid = grouid
            await self.db.update(item)

class attachment(BaseHandler):

    """
    素材
    """

    @Core_connector(form_class=AttachMentForm,model_class=AttachMent,pk_key="id")
    async def post(self,*args,**kwargs):
        pass

    @Core_connector(form_class=AttachMentForm,model_class=AttachMent,pk_key="id")
    async def put(self,*args,**kwargs):
        pass

    @Core_connector(model_class=AttachMent,pk_key="id")
    async def delete(self,*args,**kwargs):
        pass

    @Core_connector(isTransaction=False)
    async def get(self, pk=None):

        query = AttachMent.select().where(AttachMent.userid == self.user['userid'])

        if pk:
            query = query.where(AttachMent.id == pk)
        query = query.where(AttachMent.grouid == self.data.get('grouid',0))
        query = query.order_by(AttachMent.updtime.desc())

        count = len(await self.db.execute(query))

        query = query.paginate(self.data['page'], self.data['size'])

        return {
            "data":AttachMentSerializer(await self.db.execute(query),many=True).data,
            "count":count
        }

class citycode(BaseHandler):
    @Core_connector(isTransaction=False,is_query_standard=False)
    async def get(self, pk=None):
        return {"data": await datacity(redis=self.redis).get()}