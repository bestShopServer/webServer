
import json
from apps.base import BaseHandler
from utils.decorator.connector import Core_connector
from utils.exceptions import PubErrorCustom

from peewee import JOIN

from apps.web.goods.customdict import GoodsCateGoryStyleTypecode

from apps.web.goods.serializers import GoodsDetailSerializer

from models.goods import \
    GoodsCateGoryStyle,GoodsCateGory,Goods,GoodsLinkSku,GoodsLinkCity,GoodsLinkCateGory,\
        SkuGroup,SkuSpecValue

from models.setting import FareRule
from models.shop import ShopPage

from apps.web.goods.rule import GoodsCateGoryStyleRules,GoodsCateGoryRules,\
        SkuGroupRules,SkuSpecValueRules,GoodsRules,GoodsbyidsRules,GoodsLinkShopPageRules

from apps.web.shop.rule import ShopPageRules
from apps.web.shop.serializers import ShopPageDetailSerializer

from router import route

@route(None,id=True)
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

@route(None,id=True)
class goodscategory(BaseHandler):
    """
    商品分类设置
    """

    async def add_before_handler(self,**kwargs):

        try:
            gcgsObj = await self.db.get(GoodsCateGoryStyle,merchant_id=self.user.merchant_id)
        except GoodsCateGoryStyle.DoesNotExist:
            raise PubErrorCustom("请先设置分类样式!")

        if self.data.get("gdcglastid",None):
            try:
                lastcategory = await self.db.get(GoodsCateGory, gdcgid=self.data.get("gdcglastid",None), merchant_id=self.user.merchant_id)
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
        pass

    @Core_connector(**{**GoodsCateGoryRules.put(),**{"upd_before_handler":add_before_handler}})
    async def put(self, *args, **kwargs):
        pass

    @Core_connector(**{**GoodsCateGoryRules.put(),**{"del_before_handler":del_before_handler}})
    async def delete(self, *args, **kwargs):
        pass

    @Core_connector(**GoodsCateGoryRules.get())
    async def get(self, pk=None):
        pass

@route(None,id=True)
class goodsdetail(BaseHandler):

    @Core_connector(isTransaction=False)
    async def get(self, pk=None):

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

        try:
            obj.gd_fare_rule = await self.db.get(FareRule, fare_rule_id=obj.gd_fare_mould_id,merchant_id=obj.merchant_id)
        except FareRule.DoesNotExist:
            obj.gd_fare_rule = None

        query = GoodsLinkCity.select().where(GoodsLinkCity.gdid == obj.gdid)

        obj.gd_allow_area = await self.db.execute(query)

        query = GoodsLinkSku.select().where(GoodsLinkSku.id << json.loads(obj.gd_sku_links)).order_by(GoodsLinkSku.sort)

        obj.gd_sku_link = await self.db.execute(query)

        for item in obj.gd_sku_link:

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

@route(None,id=True)
class goods(BaseHandler):

    """
    商品管理
    """

    async def add_before_handler(self):
        if not isinstance(self.data['gd_sku_link'],list):
            self.data['gd_sku_link'] = json.loads(self.data['gd_sku_link'])

        self.data['gd_sku_link'].insert(0,{
            "skus":[],
            "image":self.data['gd_banners'][0][1],
            "price":self.data['gd_show_price'],
            "stock":self.data['gd_stock_tot'],
            "item_no":self.data['gd_item_no'],
            "gd_weight":self.data['gd_weight'],
            "cost_price":self.data['gd_cost_price'],
            "sort":0,
            "default":'0',
            "default_name":"默认规格"
        })

        self.data.pop("gd_stock_tot")
        self.data.pop("gd_item_no")
        self.data.pop("gd_weight")
        self.data.pop("gd_cost_price")

    @Core_connector(**{**GoodsRules.delete(),**{"add_before_handler":add_before_handler}})
    async def post(self, *args, **kwargs):
        return {"data":self.pk}

    @Core_connector(**GoodsRules.put())
    async def put(self, *args, **kwargs):
        pass

    @Core_connector(**GoodsRules.delete())
    async def delete(self, *args, **kwargs):
        pass

    @Core_connector(**GoodsRules.get())
    async def get(self, pk=None):
        pass

@route(None)
class goodsbyids(BaseHandler):
    @Core_connector(**GoodsbyidsRules.get())
    async def get(self, pk=None):
        pass

@route(None,id=True)
class goodslinkshoppage(BaseHandler):

    """
    商品详情微页面设置
    """

    async def add_after_handler(self,**kwargs):

        gdid = self.data.get("gdid")
        try:
            goodsObj = await self.db.get(Goods,gdid=gdid)
        except Goods.DoesNotExist:
            raise PubErrorCustom("商品不存在!")

        goodsObj.gd_link_shoppage = self.pk
        await self.db.update(goodsObj)

    @Core_connector(**{**ShopPageRules.post(),**{"add_after_handler":add_after_handler}})
    async def post(self, *args, **kwargs):
        return {"data":self.pk}

    @Core_connector(**ShopPageRules.put())
    async def put(self, *args, **kwargs):
        return {"data":self.pk}

    @Core_connector(isTransaction=False)
    async def get(self, pk=None):

        gdid = self.data.get("gdid")
        try:
            obj = await self.db.get(Goods,gdid=gdid)
        except Goods.DoesNotExist:
            raise PubErrorCustom("商品不存在!")

        if obj.gd_link_shoppage>0:
            try:
                return {"data":ShopPageDetailSerializer(await self.db.get(ShopPage, id=obj.gd_link_shoppage),many=False).data}
            except Goods.DoesNotExist:
                raise PubErrorCustom("详情不存在!")
        else:
            pass


@route(None,id=True)
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

@route(None,id=True)
class skuspecvalue(BaseHandler):

    """
    Sku值维护
    """

    async def add_before_handler(self,**kwargs):
        """
        新增/修改前置处理
        """
        try:
            await self.db.get(SkuGroup,group_id=self.data['group_id'],merchant_id=self.user.merchant_id)
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