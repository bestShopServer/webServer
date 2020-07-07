
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

from apps.web.goods.rule import GoodsCateGoryStyleRules,GoodsCateGoryRules,SkuGroupRules,SkuSpecValueRules

class goodscategorystyle(BaseHandler):

    """
    商品分类样式设置
    """

    async def add_before_handler(self,**kwargs):

        """
        新增/修改前置处理
        """
        for item in GoodsCateGoryStyleTypecode().data:
            if item[0] == self.data['typecode']:
                if item[1] != self.data['type']:
                    raise PubErrorCustom("分类代码和分类层级不符!")

    @Core_connector(**{**GoodsCateGoryStyleRules.post(),**{"add_before_handler":add_before_handler}})
    async def post(self, *args, **kwargs):
        pass

    @Core_connector(**{**GoodsCateGoryStyleRules.put(),**{"upd_before_handler":add_before_handler}})
    async def put(self,*args,**kwargs):
        pass

    @Core_connector(**GoodsCateGoryStyleRules.delete())
    async def delete(self,*args,**kwargs):
        pass

    @Core_connector(**GoodsCateGoryStyleRules.get())
    async def get(self, pk=None):
        pass

class goodscategory(BaseHandler):
    """
    商品分类设置
    """

    async def add_before_handler(self,**kwargs):

        try:
            gcgsObj = await self.db.get(GoodsCateGoryStyle,userid=self.user['userid'])
        except GoodsCateGoryStyle.DoesNotExist:
            raise PubErrorCustom("请先设置分类样式!")

        if self.data.get("gdcglastid",None):
            try:
                lastcategory = await self.db.get(GoodsCateGory, gdcgid=self.data.get("gdcglastid",None), userid=self.user['userid'])
                self.data['level'] = lastcategory.level+1
            except GoodsCateGory.DoesNotExist:
                raise PubErrorCustom("上级分类有误!")
        else:
            self.data['level'] = 1

        if self.data['level']>gcgsObj.type:
            raise PubErrorCustom("分类层级不能超过{}级".format(gcgsObj.type))

    async def del_before_handler(self,**kwargs):
        pk = kwargs.get("pk")

        if isinstance(pk,list):
            if len(await self.db.execute(GoodsCateGory.select().where(GoodsCateGory.gdcglastid << pk))):
                raise PubErrorCustom("分类下还存在子分类,不能直接删除!")
        else:
            if len(await self.db.execute(GoodsCateGory.select().where(GoodsCateGory.gdcglastid == pk))):
                raise PubErrorCustom("分类下还存在子分类,不能直接删除!")

    @Core_connector(**{**GoodsCateGoryRules.post(),**{"add_before_handler":add_before_handler}})
    async def post(self, *args, **kwargs):
        return {"data":kwargs.get("instance").gdcgid}

    @Core_connector(**{**GoodsCateGoryRules.put(),**{"upd_before_handler":add_before_handler}})
    async def put(self, *args, **kwargs):
        return {"data": kwargs.get("instance").gdcgid}

    @Core_connector(**{**GoodsCateGoryRules.put(),**{"del_before_handler":del_before_handler}})
    async def delete(self, *args, **kwargs):
        pass

    @Core_connector(**GoodsCateGoryRules.get())
    async def get(self, pk=None):
        pass

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

    async def del_before_handler(self,**kwargs):

        pk = kwargs.get("pk")

        if isinstance(pk,list):
            if len(await self.db.execute(SkuSpecValue.select().where(SkuSpecValue.group_id << pk))):
                raise PubErrorCustom("分组下还存在值,不能直接删除!")
        else:
            if len(await self.db.execute(SkuSpecValue.select().where(SkuSpecValue.group_id == pk))):
                raise PubErrorCustom("该分组下还存在值,不能直接删除!")

    @Core_connector(**SkuGroupRules.post())
    async def post(self,*args,**kwargs):
        pass

    @Core_connector(**SkuGroupRules.put())
    async def put(self,*args,**kwargs):
        pass

    @Core_connector(**{**SkuGroupRules.delete(),**{"del_before_handler":del_before_handler}})
    async def delete(self,*args,**kwargs):
        pass

    @Core_connector(**SkuGroupRules.get())
    async def get(self, pk=None):
        pass

class skuspecvalue(BaseHandler):

    """
    Sku值维护
    """

    async def add_before_handler(self,**kwargs):
        """
        新增/修改前置处理
        """
        try:
            await self.db.get(SkuGroup,group_id=self.data['group_id'],userid=self.user['userid'])
        except SkuGroup.DoesNotExist:
            raise PubErrorCustom("分组不存在!")

    @Core_connector(**{**SkuSpecValueRules.post(),**{"add_before_handler":add_before_handler}})
    async def post(self,*args,**kwargs):
        pass

    @Core_connector(**{**SkuSpecValueRules.put(),**{"upd_before_handler":add_before_handler}})
    async def put(self,*args,**kwargs):
        pass

    @Core_connector(**SkuSpecValueRules.delete())
    async def delete(self,*args,**kwargs):
        pass