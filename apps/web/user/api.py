from peewee import JOIN
from apps.base import BaseHandler
from utils.decorator.connector import Core_connector
from router import route

from models.user import Branch,User,UserLinkRole,UserLinkBranch,MenuLinkMerchantSetting

from utils.exceptions import PubErrorCustom

from apps.web.user.rule import BranchRules,UserRoleRules,\
            UserRoleForMenuRules,UserRoleLinkRules,MerchantRules,\
                MenuLinkMerchantSettingRules
from apps.web.user.serializers import BranchSerializer

from apps.web.user.utils import user_query

@route()
class userinfo(BaseHandler):

    """
    用户
    """

    @Core_connector()
    async def get(self, *args, **kwargs):

        return {"data": {
            "userid": self.user.userid,
            "merchant_id": self.user.merchant_id,
            "username": self.user.name,
            "rolecode": "1",
            "avatar": 'https://timgsa.baidu.com/timg?image&quality=80&size=b9999_10000&sec=1604320145113&di=c0f37be5cc6331c65ec5773edbf7c1da&imgtype=0&src=http%3A%2F%2Fb-ssl.duitang.com%2Fuploads%2Fitem%2F201703%2F18%2F20170318012043_H4mRj.jpeg',
            "menu": []
        }}

@route(None,id=True)
class branch(BaseHandler):

    """
    部门管理
    """

    @Core_connector(**BranchRules.post())
    async def post(self,*args,**kwargs):
        return {"data":self.pk}

    @Core_connector(**BranchRules.put())
    async def put(self,*args,**kwargs):
        pass

    @Core_connector(**BranchRules.delete())
    async def delete(self,*args,**kwargs):
        pass

    @Core_connector(isTicket=False)
    async def get(self, pk=None):

        parent_branch_id = self.data.get("parent_branch_id", 0)
        branch_name = self.data.get("branch_name",None)
        status = self.data.get("status",None)

        c = 0

        async def recursion(parent_branch_id,c):
            c += 1

            query = Branch.select().where(
                            Branch.parent_branch_id == parent_branch_id
                        ).order_by(Branch.sort)

            if c == 1:
                if branch_name:
                    query = query.where(Branch.branch_name == branch_name)
                if status:
                    query = query.where(Branch.status == status)

            res = await self.db.execute(
                query
            )

            child = BranchSerializer(res, many=True).data

            if not len(child):
                return

            for item in child:
                item['child'] = await recursion(item['branch_id'],c)

            return child

        return {"data": await recursion(parent_branch_id=parent_branch_id,c=c)}

@route(None,id=True)
class userrole0(BaseHandler):

    """
    系统角色管理
    """

    @Core_connector(**UserRoleRules.post())
    async def post(self,*args,**kwargs):
        return {"data":self.pk}

    @Core_connector(**UserRoleRules.put())
    async def put(self,*args,**kwargs):
        pass

    @Core_connector(**UserRoleRules.delete())
    async def delete(self,*args,**kwargs):
        pass

    @Core_connector(**UserRoleRules.get())
    async def get(self, pk=None):
        pass

@route(None,id=True)
class menu_for_role(BaseHandler):

    """
    角色获取菜单
    """

    @Core_connector(**UserRoleForMenuRules.get())
    async def get(self, pk=None):
        pass

@route(None,id=True)
class user_for_role(BaseHandler):

    """
    用户角色关联交易
    """

    @Core_connector(isTransaction=False)
    async def get(self, pk=None):

        return await user_query(
                        self=self,
                        query= User.select(User).where(User.role_type == '0')
                    )

    @Core_connector()
    async def post(self,*args,**kwargs):

        userids = self.data.get("userids")
        role_id = self.data.get("role_id")

        if not len(userids):
            raise PubErrorCustom("授权用户列表为空!")

        if not role_id:
            raise PubErrorCustom("角色代码为空!")

        for item in userids:
            await self.db.create(UserLinkRole,**{
                "role_id" : role_id,
                "userid": item
            })

    @Core_connector(**UserRoleLinkRules.delete())
    async def delete(self,*args,**kwargs):
        pass

@route(None,id=True)
class merchant(BaseHandler):

    """
    租户管理
    """

    @Core_connector(**MerchantRules.post())
    async def post(self,*args,**kwargs):
        return {"data":self.pk}

    @Core_connector(**MerchantRules.put())
    async def put(self,*args,**kwargs):
        pass

    @Core_connector(**MerchantRules.delete())
    async def delete(self,*args,**kwargs):
        pass

    @Core_connector(**MerchantRules.get())
    async def get(self, pk=None):
        pass

@route(None,id=True)
class menulinkmerchantsetting(BaseHandler):

    """
    租户规则管理
    """

    async def add_before_handler(self,**kwargs):
        """
        新增/修改前置处理
        """
        if self.data.get("default",None) and self.data.get("default")=='0':
            for item in await self.db.execute(
                    MenuLinkMerchantSetting.select().for_update().where(MenuLinkMerchantSetting.default == '0')):
                item.default = '1'
                await self.db.update(item)

    @Core_connector(**{**MenuLinkMerchantSettingRules.post(),**{"add_before_handler":add_before_handler}})
    async def post(self,*args,**kwargs):
        return {"data":self.pk}

    @Core_connector(**{**MenuLinkMerchantSettingRules.put(),**{"upd_before_handler":add_before_handler}})
    async def put(self,*args,**kwargs):
        pass

    @Core_connector(**MenuLinkMerchantSettingRules.delete())
    async def delete(self,*args,**kwargs):
        pass

    @Core_connector(**MenuLinkMerchantSettingRules.get())
    async def get(self, pk=None):
        pass