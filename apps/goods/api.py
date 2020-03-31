

from apps.base import BaseHandler
from playhouse.shortcuts import model_to_dict
from utils.decorator.connector import Core_connector
from utils.exceptions import PubErrorCustom
from models.goods import GoodsCateGory,Goods


class goodscategory(BaseHandler):

    @Core_connector()
    async def post(self, *args, **kwargs):

        self.checkmodelvoid(GoodsCateGory,['gdcgname','url','status','sort'])

        if self.data.get("gdcglastid",None):
            try:
                lastcategory = await self.db.get(GoodsCateGory, gdcgid=self.data.get("gdcglastid",None), userid=self.user['userid'])
                level = lastcategory.level+1
            except GoodsCateGory.DoesNotExist:
                raise PubErrorCustom("拒绝访问!")
        else:
            level = 1

        res = await self.db.create(
            GoodsCateGory,
            gdcgid = await self.idGeneratorClass().goodscategory(level),
            gdcgname=self.data.get("gdcgname"),
            url=self.data.get("url"),
            level=level,
            gdcglastid=self.data.get("gdcglastid",''),
            status=self.data.get("status"),
            sort=self.data.get("sort"),
            userid=self.user['userid']
        )

        return {"data":model_to_dict(res)}

    @Core_connector()
    async def put(self, pk=None):
        try:
            obj = await self.db.get(GoodsCateGory,gdcgid=pk,userid=self.user['userid'])
        except GoodsCateGory.DoesNotExist:
            raise PubErrorCustom("拒绝访问!")

        if self.data.get("gdcglastid",None):
            try:
                lastcategory = await self.db.get(GoodsCateGory, gdcgid=self.data.get("gdcglastid",None), userid=self.user['userid'])
                level = lastcategory.level+1
                obj.gdcglastid = self.data['gdcglastid']
            except GoodsCateGory.DoesNotExist:
                raise PubErrorCustom("拒绝访问!")
        else:
            level = 1

        obj.gdcgname = self.data['gdcgname']
        obj.url = self.data['url']
        obj.level = level
        obj.status = self.data['status']
        obj.sort = self.data['sort']
        await self.db.update(obj)

        return {"data":model_to_dict(obj)}

    @Core_connector()
    async def get(self, pk=None):
        query = GoodsCateGory.select().paginate(self.data['page'],self.data['size'])

        if pk:
            query = query.where(GoodsCateGory.gdcgid==pk)

        query = query.where(GoodsCateGory.userid == self.user['userid'],GoodsCateGory.level==1).order_by(GoodsCateGory.sort)

        data = [model_to_dict(item) for item in await self.db.execute(query)]

        async def recurrence(r):
            if (r and not len(r)) or not r:
                return
            for vs in r:
                vs['child']=[]
                query = GoodsCateGory.select().where(GoodsCateGory.gdcglastid == vs['gdcgid']).order_by(
                    GoodsCateGory.sort)
                inner_data = [model_to_dict(item) for item in await self.db.execute(query)]
                await recurrence(inner_data)
                vs['child']=inner_data
            return

        await recurrence(data)

        if pk:
            data = data[0] if len(data) else {}

        return {"data":data }

class goods(BaseHandler):

    @Core_connector()
    async def get(self, *args, **kwargs):
        pass