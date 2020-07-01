
import json
from apps.base import BaseHandler
from playhouse.shortcuts import model_to_dict
from utils.decorator.connector import Core_connector
from utils.exceptions import PubErrorCustom
from loguru import logger

from peewee import JOIN

from utils.time_st import UtilTime

from apps.utlis import get_response_handler

from apps.web.goods.customdict import GoodsCateGoryStyleTypecode

from apps.web.goods.forms import \
        GoodsCateGoryStyleForm,GoodsCateGoryForm,GoodsForm,\
            SkuGroupForm,SkuSpecValueForm

from apps.web.goods.serializers import \
        GoodsCateGoryStyleSerializer,GoodsCateGorySerializer,GoodsSerializer,GoodsDetailSerializer,\
            SkuGroupSerializer

from models.goods import \
    GoodsCateGoryStyle,GoodsCateGory,Goods,GoodsLinkSku,GoodsLinkCity,GoodsLinkCateGory,\
        SkuGroup,SkuSpecValue

class goodscategorystyle(BaseHandler):

    """
    商品分类样式设置
    """

    async def add_before_handler(self,obj):

        """
        新增/修改前置处理
        """
        for item in GoodsCateGoryStyleTypecode().data:
            if item[0] == obj['typecode']:
                if item[1] != obj['type']:
                    raise PubErrorCustom("分类代码和分类层级不符!")
        return obj

    @Core_connector(
        form_class=GoodsCateGoryStyleForm,
        model_class=GoodsCateGoryStyle,
        add_before_handler=add_before_handler)
    async def post(self,*args,**kwargs):
        return {"data":kwargs.get("instance").id}

    @Core_connector(
        form_class=GoodsCateGoryStyleForm,
        model_class=GoodsCateGoryStyle,
        upd_before_handler=add_before_handler,
        pk_key="id")
    async def put(self,*args,**kwargs):
        return {"data":kwargs.get("instance").id}

    @Core_connector(model_class=GoodsCateGoryStyle,pk_key="id")
    async def delete(self,*args,**kwargs):
        pass

    @Core_connector(isTransaction=False)
    async def get(self, pk=None):

        query = GoodsCateGoryStyle.select().paginate(self.data['page'],self.data['size'])
        if pk:
            query = query.where(GoodsCateGoryStyle.id == pk)

        query = query.where(GoodsCateGoryStyle.userid == self.user['userid']).order_by(GoodsCateGoryStyle.createtime.desc())


        return {"data": GoodsCateGoryStyleSerializer(await self.db.execute(query),many=True).data}

class goodscategory(BaseHandler):
    """
    商品分类设置
    """

    async def add_before_handler(self,obj):

        """
        新增/修改前置处理
        """
        try:
            gcgsObj = await self.db.get(GoodsCateGoryStyle,userid=self.user['userid'])
        except GoodsCateGoryStyle.DoesNotExist:
            raise PubErrorCustom("请先设置分类样式!")

        if self.data.get("gdcglastid",None):
            try:
                lastcategory = await self.db.get(GoodsCateGory, gdcgid=self.data.get("gdcglastid",None), userid=self.user['userid'])
                obj['level'] = lastcategory.level+1
            except GoodsCateGory.DoesNotExist:
                raise PubErrorCustom("上级分类有误!")
        else:
            obj['level'] = 1

        if obj['level']>gcgsObj.type:
            raise PubErrorCustom("分类层级不能超过{}级".format(gcgsObj.type))

        return obj

    async def del_before_handler(self,pk):

        if isinstance(pk,list):
            if len(await self.db.execute(GoodsCateGory.select().where(GoodsCateGory.gdcglastid << pk))):
                raise PubErrorCustom("分类下还存在子分类,不能直接删除!")
        else:
            if len(await self.db.execute(GoodsCateGory.select().where(GoodsCateGory.gdcglastid == pk))):
                raise PubErrorCustom("分类下还存在子分类,不能直接删除!")

    @Core_connector(
        form_class=GoodsCateGoryForm,
        model_class=GoodsCateGory,
        add_before_handler=add_before_handler)
    async def post(self, *args, **kwargs):
        return {"data":kwargs.get("instance").gdcgid}

    @Core_connector(
        form_class=GoodsCateGoryForm,
        model_class=GoodsCateGory,
        pk_key="gdcgid",
        upd_before_handler=add_before_handler)
    async def put(self, *args, **kwargs):
        return {"data": kwargs.get("instance").gdcgid}

    @Core_connector(
        model_class=GoodsCateGory,
        pk_key="gdcgid",
        del_before_handler=del_before_handler)
    async def delete(self, *args, **kwargs):
        pass

    @Core_connector(isTransaction=False)
    async def get(self, pk=None):
        query = GoodsCateGory.select().where(GoodsCateGory.userid == self.user['userid'])

        if pk:
            query = query.where(GoodsCateGory.gdcgid == pk)

        if self.data.get("gdcglastid"):
            query = query.where(GoodsCateGory.gdcglastid == self.data.get("gdcglastid"))

        query = query.order_by(GoodsCateGory.sort)

        return {"data": GoodsCateGorySerializer(await self.db.execute(query), many=True).data}

class goods(BaseHandler):

    """
    商品管理
    """

    async def add_before_handler(self,obj):

        """
        新增/修改前置处理
        """
        obj['gd_banners'] = json.dumps(obj['gd_banners'])
        return obj

    async def add_after_handler(self,obj,instance):

        """
        新增/修改后置
        """
        #区域购买处理
        if instance.gd_allow_area_flag == '0':
            await self.db.execute(GoodsLinkCity.delete().where(GoodsLinkCity.gdid==instance.gdid))
            for item in obj['gd_allow_area']:
                await self.db.create(GoodsLinkCity,**dict(
                    userid = instance.userid,
                    gdid = instance.gdid,
                    province = item.get("province",""),
                    province_name = item.get("province_name",""),
                    city = item.get("city",""),
                    city_name = item.get("city_name",""),
                    country = item.get("country",""),
                    country_name = item.get("country_name","")
                ))

        #商品分类关联处理
        await self.db.execute(GoodsLinkCateGory.delete().where(GoodsLinkCateGory.gdid==instance.gdid))
        for item in obj['gd_link_type']:
            await self.db.create(GoodsLinkCateGory,**dict(
                userid = instance.userid,
                gdid = instance.gdid,
                gdcgid = item
            ))

        #商品sku关联处理
        if instance.gd_specs_name_default_flag == '1':
            instance.gd_sku_links = []

            for index,item in enumerate(obj['gd_sku_link']):
                if item.get("id"):
                    try:
                        link_sku_obj = await self.db.get(GoodsLinkSku,id=item.get("id"))
                        link_sku_obj.userid=instance.userid,
                        link_sku_obj.gdid=instance.gdid,
                        link_sku_obj.skus=json.dumps(item['skus'])
                        link_sku_obj.image = item.get("image","")
                        link_sku_obj.price = item.get("price",0.0)
                        link_sku_obj.stock = item.get("stock",0)
                        link_sku_obj.item_no = item.get("item_no","")
                        link_sku_obj.weight = item.get("weight",0)
                        link_sku_obj.cost_price = item.get("cost_price",0.0)
                        # link_sku_obj.number = item.get("number",0)
                        link_sku_obj.sort = index+1
                        self.db.update(link_sku_obj)
                    except GoodsLinkSku.DoesNotExist:
                        raise PubErrorCustom("sku关联id[{}]是无效的!".format(item.get("id")))
                else:
                    link_sku_obj = await self.db.create(GoodsLinkSku,**dict(
                        userid=instance.userid,
                        gdid=instance.gdid,
                        skus=json.dumps(item['skus']),
                        image = item.get("image",""),
                        price = item.get("price",0.0),
                        stock = item.get("stock",0),
                        item_no = item.get("item_no",""),
                        weight = item.get("weight",0),
                        cost_price = item.get("cost_price",0.0),
                        # number = item.get("number",0),
                        sort = index+1
                    ))
                instance.gd_sku_links.append(link_sku_obj.id)
            await self.db.update(instance)
        return instance

    async def del_before_handler(self,pk):
        pass

    @Core_connector(
        form_class=GoodsForm,
        model_class=Goods,
        add_before_handler=add_before_handler,
        add_after_handler=add_after_handler)
    async def post(self, *args, **kwargs):
        return {"data": kwargs.get("instance").gdid}

    @Core_connector(
        form_class=GoodsForm,
        model_class=Goods,
        pk_key="gdid",
        upd_before_handler=add_before_handler,
        upd_after_handler=add_after_handler)
    async def put(self, *args, **kwargs):
        return {"data":kwargs.get("instance").gdid}

    @Core_connector(
        model_class=Goods,
        pk_key="gdid",
        del_before_handler=del_before_handler)
    async def delete(self, *args, **kwargs):
        pass

    @Core_connector(isTransaction=False,is_query_standard=False)
    async def get(self, pk=None):

        #查询详情
        if self.data.get('detail'):
            if not pk:
                raise PubErrorCustom("查询详情时商品ID不能为空!")

            try:
                obj = await self.db.get(Goods, gdid=pk)
            except Goods.DoesNotExist:
                raise PubErrorCustom("此商品不存在!")

            query = GoodsLinkCateGory.select(GoodsLinkCateGory,GoodsCateGory.gdcgname). \
                join(GoodsCateGory, join_type=JOIN.INNER, on=(GoodsLinkCateGory.gdcgid == GoodsCateGory.gdcgid)).\
                where(GoodsLinkCateGory.gdid == obj.gdid,GoodsCateGory.status == '0')

            obj.gd_link_type = await self.db.execute(query)

            # logger.info(obj.gd_link_type)
            query = GoodsLinkCity.select().where(GoodsLinkCity.gdid == obj.gdid)

            obj.gd_allow_area = await self.db.execute(query)

            query = GoodsLinkSku.select().where(GoodsLinkSku.id << json.loads(obj.gd_sku_links)).order_by(GoodsLinkSku.sort)

            obj.gd_sku_links = await self.db.execute(query)

            for item in obj.gd_sku_links:

                skus = []

                for skuItem in json.loads(item.skus):

                    try:
                        skuGroupObj = await self.db.get(SkuGroup, group_id=skuItem['group_id'])
                    except SkuGroup.DoesNotExist:
                        skuGroupObj = None

                    try:
                        skuSpecValueObj = await self.db.get(SkuSpecValue, spec_id=skuItem['spec_id'])
                    except SkuGroup.DoesNotExist:
                        skuSpecValueObj = None

                    if skuGroupObj and skuSpecValueObj and skuSpecValueObj.group_id == skuGroupObj.group_id:
                        skus.append(dict(
                            group_id = skuSpecValueObj.group_id,
                            spec_id = skuSpecValueObj.spec_id,
                            group_name = skuGroupObj.group_name,
                            spec_value = skuSpecValueObj.spec_value
                        ))

                item.skus = skus

            return {"data": GoodsDetailSerializer([obj], many=True).data[0]}

        #查询列表
        else:
            query = Goods.select().where(Goods.userid == self.user['userid'])

            if self.data.get("gdcgids"):
                gdids = [ item.gdid for item in await self.db.execute(GoodsCateGory.select().where(GoodsCateGory.gdcgid << self.data.get("gdcgids"))) ]
                query = query.where(Goods.gdid << gdids)

            if self.data.get("start_datetime") and self.data.get("end_datetime"):
                ut = UtilTime()
                start_datetime = ut.string_to_timestamp(self.data.get("start_datetime"))
                end_datetime = ut.string_to_timestamp(self.data.get("end_datetime"))

                query = query.where(Goods.createtime>=start_datetime,Goods.createtime<=end_datetime)

            query = query.order_by(Goods.createtime.desc())

            count = len(await self.db.execute(query))

            query = query.paginate(self.data['page'], self.data['size'])

            return {
                "data": GoodsSerializer(await self.db.execute(query), many=True).data,
                "count":count
            }

class skugroup(BaseHandler):

    """
    Sku分组维护
    """

    async def del_before_handler(self,pk):

        if isinstance(pk,list):
            if len(await self.db.execute(SkuSpecValue.select().where(SkuSpecValue.group_id << pk))):
                raise PubErrorCustom("分组下还存在值,不能直接删除!")
        else:
            if len(await self.db.execute(SkuSpecValue.select().where(SkuSpecValue.group_id == pk))):
                raise PubErrorCustom("该分组下还存在值,不能直接删除!")

    @Core_connector(
        form_class=SkuGroupForm,
        model_class=SkuGroup)
    async def post(self,*args,**kwargs):
        return {"data":kwargs.get("instance").group_id}

    @Core_connector(
        form_class=SkuGroupForm,
        model_class=SkuGroup,
        pk_key="group_id")
    async def put(self,*args,**kwargs):
        return {"data":kwargs.get("instance").group_id}

    @Core_connector(
        model_class=SkuGroup,
        del_before_handler=del_before_handler,
        pk_key="group_id"
    )
    async def delete(self,*args,**kwargs):
        pass

    @Core_connector(isTransaction=False)
    async def get(self, pk=None):

        query = SkuGroup.select().where(SkuGroup.userid == self.user['userid'])

        if pk:
            query = query.where(SkuGroup.group_id == pk)

        count = len(await self.db.execute(query))

        query  = query.paginate(self.data['page'], self.data['size'])

        skugroupObj = await self.db.execute(query)

        for item in skugroupObj:
            item.spec_values = await self.db.execute(SkuSpecValue.select().where(SkuSpecValue.group_id == item.group_id ))

        return {"data": SkuGroupSerializer(skugroupObj,many=True).data,"count":count}

class skuspecvalue(BaseHandler):

    """
    Sku值维护
    """

    async def add_before_handler(self,obj):

        """
        新增/修改前置处理
        """
        try:
            await self.db.get(SkuGroup,group_id=obj['group_id'],userid=self.user['userid'])
        except SkuGroup.DoesNotExist:
            raise PubErrorCustom("分组不存在!")

        return obj

    @Core_connector(
        form_class=SkuSpecValueForm,
        model_class=SkuSpecValue,
        add_before_handler=add_before_handler)
    async def post(self,*args,**kwargs):
        return {"data": kwargs.get("instance").spec_id}

    @Core_connector(
        form_class=SkuSpecValueForm,
        model_class=SkuSpecValue,
        upd_before_handler=add_before_handler,
        pk_key="spec_id")
    async def put(self,*args,**kwargs):
        return {"data":kwargs.get("instance").spec_id}

    @Core_connector(model_class=SkuSpecValue,pk_key="spec_id")
    async def delete(self,*args,**kwargs):
        pass


# class goodscategory(BaseHandler):
#     """
#     商品分类
#     """
#
#     @Core_connector()
#     async def post(self):
#
#         self.checkmodelvoid(GoodsCateGory,['gdcgname','url','status','sort'])
#
#         if self.data.get("gdcglastid",None):
#             try:
#                 lastcategory = await self.db.get(GoodsCateGory, gdcgid=self.data.get("gdcglastid",None), userid=self.user['userid'])
#                 level = lastcategory.level+1
#             except GoodsCateGory.DoesNotExist:
#                 raise PubErrorCustom("拒绝访问!")
#         else:
#             level = 1
#
#         res = await self.db.create(
#             GoodsCateGory,
#             gdcgid = await self.idGeneratorClass().goodscategory(level),
#             gdcgname=self.data.get("gdcgname"),
#             url=self.data.get("url"),
#             level=level,
#             gdcglastid=self.data.get("gdcglastid",''),
#             status=self.data.get("status"),
#             sort=self.data.get("sort"),
#             userid=self.user['userid']
#         )
#
#         return {"data":model_to_dict(res)}
#
#     @Core_connector()
#     async def put(self, pk=None):
#         try:
#             obj = await self.db.get(GoodsCateGory,gdcgid=pk,userid=self.user['userid'])
#         except GoodsCateGory.DoesNotExist:
#             raise PubErrorCustom("拒绝访问!")
#
#         if self.data.get("gdcglastid",None):
#             try:
#                 lastcategory = await self.db.get(GoodsCateGory, gdcgid=self.data.get("gdcglastid",None), userid=self.user['userid'])
#                 level = lastcategory.level+1
#                 obj.gdcglastid = self.data['gdcglastid']
#             except GoodsCateGory.DoesNotExist:
#                 raise PubErrorCustom("拒绝访问!")
#         else:
#             level = 1
#
#         obj.gdcgname = self.data['gdcgname']
#         obj.url = self.data['url']
#         obj.level = level
#         obj.status = self.data['status']
#         obj.sort = self.data['sort']
#         await self.db.update(obj)
#
#         return {"data":model_to_dict(obj)}
#
#     @Core_connector()
#     async def get(self, pk=None):
#         query = GoodsCateGory.select().paginate(self.data['page'],self.data['size'])
#
#         if pk:
#             query = query.where(GoodsCateGory.gdcgid==pk)
#
#         query = query.where(GoodsCateGory.userid == self.user['userid'],GoodsCateGory.level==1).order_by(GoodsCateGory.sort)
#
#         data = [model_to_dict(item) for item in await self.db.execute(query)]
#
#         async def recurrence(r):
#             if (r and not len(r)) or not r:
#                 return
#             for vs in r:
#                 vs['child']=[]
#                 query = GoodsCateGory.select().where(GoodsCateGory.gdcglastid == vs['gdcgid']).order_by(
#                     GoodsCateGory.sort)
#                 inner_data = [model_to_dict(item) for item in await self.db.execute(query)]
#                 await recurrence(inner_data)
#                 vs['child']=inner_data
#             return
#
#         await recurrence(data)
#
#         if pk:
#             data = data[0] if len(data) else {}
#
#         return {"data":data }
#
#     @Core_connector()
#     async def delete(self,pk=None):
#         try:
#             group = await self.db.get(GoodsCateGory,gdcgid=pk,userid=self.user['userid'])
#         except GoodsCateGory.DoesNotExist:
#             raise PubErrorCustom("拒绝访问!")
#
#         await self.db.delete(group)
#
#         return None
#
# class goods(BaseHandler):
#
#     """
#     商品
#     """
#
#     @Core_connector()
#     async def post(self):
#
#         self.checkmodelvoid(Goods,['gdname','sort'])
#
#         gdotherinfo={
#             "sharememo":self.data.get("sharememo",""),
#             "selltype":self.data.get("selltype",""),
#             "uptime":self.data.get("uptime",""),
#             "willsell":{
#                 "flag":self.data.get("willsellflag",'0'),
#                 "type":self.data.get("willselltype",''),
#                 "value": self.data.get("willsellvalue",''),
#             },
#             "limitsell": {
#                 "flag": self.data.get("limitsellflag", '0'),
#                 "type": self.data.get("limitselltype", ''),
#                 "value": self.data.get("limitsellvalue", ''),
#             }
#         }
#
#         createdata={
#             "gdid": await self.idGeneratorClass().goods(),
#             "gdname" : self.data['gdname'],
#             'sort' : self.data['sort'],
#             'gdbanners':json.dumps({"gdbanners":self.data.get('gdbanners',[])}),
#             "gdcgid":json.dumps({"gdcgids":self.data.get('gdcgid',[])}),
#             "gdshowprice":self.data.get("gdshowprice","0.0"),
#             "gdshowprice1":self.data.get("gdshowprice1","0.0"),
#             "gdstockdeltype":self.data.get("gdstockdeltype","1"),
#             "gdhavetime":self.data.get("gdhavetime",0),
#             "gdresidueshow":self.data.get("gdresidueshow",'0'),
#             "gdotherinfo":json.dumps(gdotherinfo),
#             "userid":self.user['userid'],
#             "gdsku":{"gdsku":[]}
#         }
#
#         if self.data.get("uptimeflag",None) == '0':
#             createdata['gdstatus'] = '0'
#         elif self.data.get("uptimeflag",None) == '1':
#             """
#                 此处逻辑暂时未写,添加商品定时上架到定时任务!
#             """
#
#         """
#             Sku处理
#         """
#         for item in self.data.get("gdsku", []):
#             tmp = await self.db.create(GoodsLinkSku,
#                      gdid=createdata['gdid'],
#                      keyid=item['keyid'],
#                      valueid=item['valueid'],
#                      price=item.get("price", 0.0),
#                      img=item.get("img", ""),
#                      stock=item.get("stock", 0),
#                      code=item.get("code", ""),
#                      cost_price=item.get("cost_price", 0.0))
#             createdata['gdsku']['gdsku'].append(tmp.id)
#
#         createdata['gdsku'] = json.dumps(createdata['gdsku'])
#         print(createdata)
#         await self.db.create(Goods,**createdata)
#         return None
#
#
#     @Core_connector()
#     async def put(self, pk=None):
#
#         try:
#             obj = await self.db.get(Goods,gdid=pk,userid=self.user['userid'])
#         except Goods.DoesNotExist:
#             raise PubErrorCustom("拒绝访问!")
#
#         obj.gdotherinfo = json.loads(obj.gdotherinfo)
#
#         if self.data.get("gdname",None):
#             obj.gdname = self.data['gdname']
#         if self.data.get("sort",None):
#             obj.sort = self.data['sort']
#         if self.data.get("sharememo",None):
#             obj.gdotherinfo['sharememo'] = self.data['sharememo']
#         if self.data.get("gdbanners",None):
#             obj.gdbanners = json.dumps({"gdbanners":self.data.get('gdbanners',[])})
#         if self.data.get("gdcgid",None):
#             obj.gdcgid = json.dumps({"gdcgids":self.data.get('gdcgid',[])})
#         if self.data.get("selltype",None):
#             obj.gdotherinfo['selltype'] = self.data['selltype']
#         if self.data.get("gdshowprice", None):
#             obj.gdshowprice = self.data['gdshowprice']
#         if self.data.get("gdshowprice1", None):
#             obj.gdshowprice1 = self.data['gdshowprice1']
#         if self.data.get("gdstockdeltype", None):
#             obj.gdstockdeltype = self.data['gdstockdeltype']
#         if self.data.get("gdhavetime", None):
#             obj.gdhavetime = self.data['gdhavetime']
#         if self.data.get("gdresidueshow", None):
#             obj.gdresidueshow = self.data['gdresidueshow']
#         if self.data.get("uptimeflag", None):
#             obj.gdstatus = self.data['uptimeflag']
#         if self.data.get("uptime",None):
#             obj.gdotherinfo['uptime'] = self.data['uptime']
#         if self.data.get("willsellflag",None):
#             obj.gdotherinfo['willsell']['flag'] = self.data['willsellflag']
#         if self.data.get("willselltype",None):
#             obj.gdotherinfo['willsell']['type'] = self.data['willselltype']
#         if self.data.get("willsellvalue",None):
#             obj.gdotherinfo['willsell']['value'] = self.data['willsellvalue']
#         if self.data.get("limitsellflag",None):
#             obj.gdotherinfo['limitsell']['flag'] = self.data['limitsellflag']
#         if self.data.get("limitselltype",None):
#             obj.gdotherinfo['limitsell']['type'] = self.data['limitselltype']
#         if self.data.get("limitsellvalue",None):
#             obj.gdotherinfo['limitsell']['value'] = self.data['limitsellvalue']
#
#         if self.data.get("gdsku",None):
#             gdsku = json.loads(obj.gdsku)['gdsku']
#             haves=[]
#             for item in self.data.get("gdsku",None):
#                 if 'id' not in item:
#                     tmp = await self.db.create(GoodsLinkSku,
#                            gdid=obj.gdid,
#                            keyid=item['keyid'],
#                            valueid=item['valueid'],
#                            price=item.get("price", 0.0),
#                            img=item.get("img", ""),
#                            stock=item.get("stock", 0),
#                            code=item.get("code", ""),
#                            cost_price=item.get("cost_price", 0.0))
#                     gdsku.append(tmp.id)
#                     haves.append(tmp.id)
#                 else:
#                     if item['id'] in gdsku:
#                         haves.append(item['id'])
#                         try:
#                             goodslinkSkuObj = await self.db.get(GoodsLinkSku, id=item['id'])
#                             goodslinkSkuObj.keyid = item['keyid']
#                             goodslinkSkuObj.valueid = item['valueid']
#                             goodslinkSkuObj.price = item.get("price", 0.0)
#                             goodslinkSkuObj.img = item.get("img", "")
#                             goodslinkSkuObj.stock = item.get("stock", 0)
#                             goodslinkSkuObj.code = item.get("code", "")
#                             goodslinkSkuObj.cost_price = item.get("cost_price", 0.0)
#                             await self.db.update(goodslinkSkuObj)
#                         except GoodsLinkSku.DoesNotExist:
#                             raise PubErrorCustom("拒绝访问!")
#                     else:
#                         raise PubErrorCustom("拒绝访问!")
#
#             for item in list(set(gdsku).difference(set(haves))):
#                 try:
#                     dGLs = await self.db.get(GoodsLinkSku, id=item)
#                 except GoodsLinkSku.DoesNotExist:
#                     raise PubErrorCustom("拒绝访问!")
#                 await self.db.delete(dGLs)
#                 return None
#
#             obj.gdsku = json.dumps({"gdsku":haves})
#
#         obj.gdotherinfo = json.dumps(obj.gdotherinfo)
#
#         await self.db.update(obj)
#
#         return None
#
#     @Core_connector()
#     async def get(self, pk=None):
#         query = Goods.select().where(Goods.userid == self.user['userid'])
#
#         if pk:
#             query = query.where(Goods.gdid == pk)
#
#         count = len(await self.db.execute(query))
#
#         query = query.paginate(self.data['page'], self.data['size'])
#
#         data=[]
#         for item in await self.db.execute(query):
#
#             gdotherinfo = json.loads(item.gdotherinfo)
#
#             skuQuery = GoodsLinkSku.select(GoodsLinkSku,SkuKey,SkuValue). \
#                 join(SkuKey, join_type=JOIN.INNER, on=(GoodsLinkSku.keyid == SkuKey.id)).\
#                 join(SkuValue, join_type=JOIN.INNER, on=(GoodsLinkSku.valueid == SkuValue.id)).\
#                 where(GoodsLinkSku.gdid << json.loads(item.gdsku)['gdsku'] )
#
#             sku=[]
#             for skuItem in await self.db.execute(skuQuery):
#                 t=model_to_dict(skuItem)
#                 t['key'] = skuItem.skukey.key
#                 t['value'] = skuItem.skukey.skuvalue.value
#                 sku.append(t)
#
#             data.append({
#                 "gdid":item.gdid,
#                 "gdname":item.gdname,
#                 "sharememo":gdotherinfo['sharememo'],
#                 "gdbanners":json.loads(item.gdbanners)['gdbanners'],
#                 "gdcgid":json.loads(item.gdcgid)['gdcgids'],
#                 "selltype":gdotherinfo['selltype'],
#                 "gdsku": sku,
#                 "gdshowprice":item.gdshowprice,
#                 "gdshowprice1":item.gdshowprice1,
#                 "gdstockdeltype":item.gdstockdeltype,
#                 "gdhavetime":item.gdhavetime,
#                 "gdresidueshow":item.gdresidueshow,
#                 "uptimeflag":item.gdstatus,
#                 "uptime":gdotherinfo['uptime'],
#                 "willsellflag":gdotherinfo['willsell']['flag'],
#                 "willselltype":gdotherinfo['willsell']['type'],
#                 "willsellvalue":gdotherinfo['willsell']['value'],
#                 "limitsellflag":gdotherinfo['limitsell']['flag'],
#                 "limitselltype": gdotherinfo['limitsell']['type'],
#                 "limitsellvalue": gdotherinfo['limitsell']['value'],
#             })
#
#         if pk:
#             data = data[0] if len(data) else {}
#
#         return {"data": data,"count":count}
#
#
#     @Core_connector()
#     async def delete(self,pk=None):
#         try:
#             group = await self.db.get(Goods,gdid=pk,userid=self.user['userid'])
#         except Goods.DoesNotExist:
#             raise PubErrorCustom("拒绝访问!")
#
#         await self.db.delete(group)
#
#         return None
#
# class skugroup(BaseHandler):
#     """
#     sku组维护
#     """
#
#     @Core_connector()
#     async def post(self):
#
#         self.checkmodelvoid(SkuKey,['key'])
#
#         res = await self.db.create(
#             SkuKey,
#             userid=self.user['userid'],
#             key=self.data['key']
#         )
#
#         return {"data": model_to_dict(res)}
#
#     @Core_connector()
#     async def put(self, pk=None):
#
#
#         try:
#             obj = await self.db.get(SkuKey,id=pk,userid=self.user['userid'])
#         except SkuKey.DoesNotExist:
#             raise PubErrorCustom("拒绝访问!")
#
#         obj.key = self.data['key']
#         await self.db.update(obj)
#         return {"data": model_to_dict(obj)}
#
#     @Core_connector()
#     async def delete(self,pk=None):
#         try:
#             group = await self.db.get(SkuKey,id=pk,userid=self.user['userid'])
#         except SkuKey.DoesNotExist:
#             raise PubErrorCustom("拒绝访问!")
#
#         await self.db.delete(group)
#
#         return None
#
#     @Core_connector()
#     async def get(self, pk=None):
#         query = SkuKey.select()
#
#         if pk:
#             query = query.where(SkuKey.id == pk)
#
#         query = query.where(SkuKey.userid == self.user['userid'])
#
#         count = len(await self.db.execute(query))
#
#         query = query.paginate(self.data['page'], self.data['size'])
#         # logger.info(query)
#         data = [model_to_dict(item)  for item in await self.db.execute(query) ]
#
#         for item in data:
#             query = SkuValue.select().where(SkuValue.keyid == item['id'] )
#             item['data'] = [model_to_dict(item)  for item in await self.db.execute(query) ]
#
#         if pk:
#             data = data[0] if len(data) else {}
#
#         return {"data": data,"count":count}
#
# class sku(BaseHandler):
#     """
#     sku值维护
#     """
#
#     @Core_connector()
#     async def post(self):
#
#         self.checkmodelvoid(SkuValue,['keyid','value'])
#
#         res = await self.db.create(
#             SkuValue,
#             userid=self.user['userid'],
#             keyid=self.data['keyid'],
#             value = self.data['value']
#         )
#
#         return {"data": model_to_dict(res)}
#
#     @Core_connector()
#     async def put(self, pk=None):
#
#         try:
#             obj = await self.db.get(SkuValue,id=pk,userid=self.user['userid'])
#         except SkuValue.DoesNotExist:
#             raise PubErrorCustom("拒绝访问!")
#
#         obj.value = self.data['value']
#         await self.db.update(obj)
#         return {"data": model_to_dict(obj)}
#
#     @Core_connector()
#     async def delete(self,pk=None):
#         try:
#             group = await self.db.get(SkuValue,id=pk,userid=self.user['userid'])
#         except SkuValue.DoesNotExist:
#             raise PubErrorCustom("拒绝访问!")
#
#         await self.db.delete(group)
#
#         return None
#
#     @Core_connector()
#     async def get(self, pk=None):
#         query = SkuValue.select().paginate(self.data['page'], self.data['size'])
#
#         if pk:
#             query = query.where(SkuValue.id == pk)
#
#         if self.data.get("keyid",None):
#             query = query.where(SkuValue.keyid == self.self.data.get("keyid",None))
#
#         query = query.where(SkuValue.userid == self.user['userid'])
#
#         data = [model_to_dict(item) for item in await self.db.execute(query)]
#
#         if pk:
#             data = data[0] if len(data) else {}
#
#         return {"data": data}