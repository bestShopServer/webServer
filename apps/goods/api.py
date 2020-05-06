
import json
from apps.base import BaseHandler
from playhouse.shortcuts import model_to_dict
from utils.decorator.connector import Core_connector
from utils.exceptions import PubErrorCustom
from models.goods import GoodsCateGory,Goods,SkuKey,SkuValue,GoodsLinkSku
from peewee import *
from decimal import *

class goodscategory(BaseHandler):
    """
    商品分类
    """

    @Core_connector()
    async def post(self):

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

    @Core_connector()
    async def delete(self,pk=None):
        try:
            group = await self.db.get(GoodsCateGory,gdcgid=pk,userid=self.user['userid'])
        except GoodsCateGory.DoesNotExist:
            raise PubErrorCustom("拒绝访问!")

        await self.db.delete(group)

        return None

class goods(BaseHandler):

    """
    商品
    """

    @Core_connector()
    async def post(self):

        self.checkmodelvoid(Goods,['gdname','sort'])

        gdotherinfo={
            "sharememo":self.data.get("sharememo",""),
            "selltype":self.data.get("selltype",""),
            "uptime":self.data.get("uptime",""),
            "willsell":{
                "flag":self.data.get("willsellflag",'0'),
                "type":self.data.get("willselltype",''),
                "value": self.data.get("willsellvalue",''),
            },
            "limitsell": {
                "flag": self.data.get("limitsellflag", '0'),
                "type": self.data.get("limitselltype", ''),
                "value": self.data.get("limitsellvalue", ''),
            }
        }

        createdata={
            "gdid": await self.idGeneratorClass().goods(),
            "gdname" : self.data['gdname'],
            'sort' : self.data['sort'],
            'gdbanners':json.dumps({"gdbanners":self.data.get('gdbanners',[])}),
            "gdcgid":json.dumps({"gdcgids":self.data.get('gdcgid',[])}),
            "gdshowprice":self.data.get("gdshowprice","0.0"),
            "gdshowprice1":self.data.get("gdshowprice1","0.0"),
            "gdstockdeltype":self.data.get("gdstockdeltype","1"),
            "gdhavetime":self.data.get("gdhavetime",0),
            "gdresidueshow":self.data.get("gdresidueshow",'0'),
            "gdsku":json.dumps({"gdsku":self.data.get("gdsku",[])}),
            "gdotherinfo":json.dumps(gdotherinfo),
            "userid":self.user['userid']
        }

        if self.data.get("uptimeflag",None) == '0':
            createdata['gdstatus'] = '0'
        elif self.data.get("uptimeflag",None) == '1':
            """
                此处逻辑暂时未写,添加商品定时上架到定时任务!
            """
        print(createdata)
        goodsObj = await self.db.create(Goods,**createdata)

        """
            Sku处理
        """
        for item in self.data.get("gdsku",[]):
            await self.db.create(GoodsLinkSku,
                 gdid = goodsObj.gdid,
                 keyid = item['keyid'],
                 valueid=item['valueid'],
                 price = item.get("price",0.0),
                 img = item.get("img",""),
                 stock = item.get("stock",0),
                 code = item.get("code",""),
                 cost_price = item.get("cost_price",0.0))

        return None

    @Core_connector()
    async def get(self, pk=None):
        query = Goods.select().where(Goods.userid == self.user['userid'])

        if pk:
            query = query.where(Goods.gdid == pk)

        data=[]
        for item in await self.db.execute(query):

            gdotherinfo = json.loads(item.gdotherinfo)

            skuQuery = GoodsLinkSku.select(GoodsLinkSku,SkuKey,SkuValue). \
                join(SkuKey, join_type=JOIN.INNER, on=(GoodsLinkSku.keyid == SkuKey.id)).\
                join(SkuValue, join_type=JOIN.INNER, on=(GoodsLinkSku.valueid == SkuValue.id)).\
                where(GoodsLinkSku.gdid == item.gdid )

            data.append({
                "gdname":item.gdname,
                "sharememo":gdotherinfo['sharememo'],
                "gdbanners":json.loads(item.gdbanners)['gdbanners'],
                "gdcgid":json.loads(item.gdcgid)['gdcgids'],
                "selltype":gdotherinfo['selltype'],
                "gdsku": [model_to_dict(item)  for item in await self.db.execute(skuQuery) ],
                "gdshowprice":item.gdshowprice,
                "gdshowprice1":item.gdshowprice1,
                "gdstockdeltype":item.gdstockdeltype,
                "gdhavetime":item.gdhavetime,
                "gdresidueshow":item.gdresidueshow,
                "uptimeflag":item.gdstatus,
                "uptime":gdotherinfo['uptime'],
                "willsellflag":gdotherinfo['willsell']['flag'],
                "willselltype":gdotherinfo['willsell']['type'],
                "willsellvalue":gdotherinfo['willsell']['value'],
                "limitsellflag":gdotherinfo['limitsell']['flag'],
                "limitselltype": gdotherinfo['limitsell']['type'],
                "limitsellvalue": gdotherinfo['limitsell']['value'],
            })

        if pk:
            data = data[0] if len(data) else {}

        return {"data": data}


class skugroup(BaseHandler):
    """
    sku组维护
    """

    @Core_connector()
    async def post(self):

        self.checkmodelvoid(SkuKey,['key'])

        res = await self.db.create(
            SkuKey,
            userid=self.user['userid'],
            key=self.data['key']
        )

        return {"data": model_to_dict(res)}

    @Core_connector()
    async def put(self, pk=None):


        try:
            obj = await self.db.get(SkuKey,id=pk,userid=self.user['userid'])
        except SkuKey.DoesNotExist:
            raise PubErrorCustom("拒绝访问!")

        obj.key = self.data['key']
        await self.db.update(obj)
        return {"data": model_to_dict(obj)}

    @Core_connector()
    async def delete(self,pk=None):
        try:
            group = await self.db.get(SkuKey,id=pk,userid=self.user['userid'])
        except SkuKey.DoesNotExist:
            raise PubErrorCustom("拒绝访问!")

        await self.db.delete(group)

        return None

    @Core_connector()
    async def get(self, pk=None):
        query = SkuKey.select()

        if pk:
            query = query.where(SkuKey.id == pk)

        query = query.where(SkuKey.userid == self.user['userid'])

        count = len(await self.db.execute(query))

        query = query.paginate(self.data['page'], self.data['size'])
        # logger.info(query)
        data = [model_to_dict(item)  for item in await self.db.execute(query) ]

        for item in data:
            query = SkuValue.select().where(SkuValue.keyid == item['id'] )
            item['data'] = [model_to_dict(item)  for item in await self.db.execute(query) ]

        if pk:
            data = data[0] if len(data) else {}

        return {"data": data,"count":count}

class sku(BaseHandler):
    """
    sku值维护
    """

    @Core_connector()
    async def post(self):

        self.checkmodelvoid(SkuValue,['keyid','value'])

        res = await self.db.create(
            SkuValue,
            userid=self.user['userid'],
            keyid=self.data['keyid'],
            value = self.data['value']
        )

        return {"data": model_to_dict(res)}

    @Core_connector()
    async def put(self, pk=None):

        try:
            obj = await self.db.get(SkuValue,id=pk,userid=self.user['userid'])
        except SkuValue.DoesNotExist:
            raise PubErrorCustom("拒绝访问!")

        obj.value = self.data['value']
        await self.db.update(obj)
        return {"data": model_to_dict(obj)}

    @Core_connector()
    async def delete(self,pk=None):
        try:
            group = await self.db.get(SkuValue,id=pk,userid=self.user['userid'])
        except SkuValue.DoesNotExist:
            raise PubErrorCustom("拒绝访问!")

        await self.db.delete(group)

        return None

    @Core_connector()
    async def get(self, pk=None):
        query = SkuValue.select().paginate(self.data['page'], self.data['size'])

        if pk:
            query = query.where(SkuValue.id == pk)

        if self.data.get("keyid",None):
            query = query.where(SkuValue.keyid == self.self.data.get("keyid",None))

        query = query.where(SkuValue.userid == self.user['userid'])

        data = [model_to_dict(item) for item in await self.db.execute(query)]

        if pk:
            data = data[0] if len(data) else {}

        return {"data": data}