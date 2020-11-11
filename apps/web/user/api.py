from peewee import JOIN
from apps.base import BaseHandler
from utils.decorator.connector import Core_connector
from router import route
from loguru import logger
from models.user import Branch,User,UserLinkRole,UserLinkBranch,\
                            MenuLinkMerchantSetting,UserAuth,UserRole,\
                                UserLinkMerchant,Merchant

from utils.exceptions import PubErrorCustom

from apps.web.user.rule import BranchRules,UserRoleRules,\
            UserRoleForMenuRules,UserRoleLinkRules,MerchantRules,\
                MenuLinkMerchantSettingRules,UserRules
from apps.web.user.serializers import BranchSerializer

from apps.web.user.utils import user_query

@route()
class userinfo(BaseHandler):

    """
    用户
    """

    async def merchant_token_handler(self):

        merchant_id = self.data.get("merchant_id",None)
        if not merchant_id:
            raise PubErrorCustom("租户ID为空")

        redis_cli = self.redisC(key=self.token)
        response = await redis_cli.get_dict()
        response['merchant_id'] = merchant_id
        await redis_cli.set_dict(response)
        return response

    @Core_connector()
    async def get(self, pk=None):

        merchant_obj=None
        if self.user.role_type == '1':
            merchant_obj = await self.merchant_token_handler()

        return {"data": {
            "userid": self.user.userid,
            "merchant_id": merchant_obj['merchant_id'] if merchant_obj else 0,
            "username": self.user.name,
            "rolecode": "",
            "avatar": 'https://timgsa.baidu.com/timg?image&quality=80&size=b9999_10000&sec=1604320145113&di=c0f37be5cc6331c65ec5773edbf7c1da&imgtype=0&src=http%3A%2F%2Fb-ssl.duitang.com%2Fuploads%2Fitem%2F201703%2F18%2F20170318012043_H4mRj.jpeg',
            "menu": []
        }}

@route(None,id=True)
class user(BaseHandler):

    """
    用户管理
    """

    async def add_after_handler(self,**kwargs):

        mobile = self.data.get("mobile",None)
        email = self.data.get("email",None)
        login_name = self.data.get("login_name", None)

        async def createUserAuth(account,type):
            if await self.db.count(
                    UserAuth.select().where(UserAuth.account == account, UserAuth.type == type)) > 0:
                if type == '0':
                    raise PubErrorCustom("登录账号已存在!")
                elif type == '1':
                    raise PubErrorCustom("手机号已存在!")
                elif type == '2':
                    raise PubErrorCustom("邮箱已存在!")

            await self.db.create(UserAuth, **{
                "userid": self.pk,
                "type": type,
                "account": account,
                "ticket": self.data.get("password")
            })

        if mobile:
            await createUserAuth(account=mobile,type="1")

        if email:
            await createUserAuth(account=email,type="2")

        if login_name:
            await createUserAuth(account=login_name,type="0")

    async def upd_before_handler(self,**kwargs):

        pk = kwargs.get("pk")

        mobile = self.data.get("mobile", None)
        email = self.data.get("email", None)
        login_name = self.data.get("login_name", None)
        password = self.data.get("password")

        if password:
            await self.db.execute(
                UserAuth.update({
                    UserAuth.ticket : password
                }).where(
                    UserAuth.userid == pk,
                    UserAuth.is_password == '0'
                )
            )

        async def updUserAuth(account, type,pk):

            if await self.db.count(
                    UserAuth.select().where(
                        UserAuth.account == account,
                        UserAuth.type == type,
                        UserAuth.userid != pk)) > 0:
                if type == '0':
                    raise PubErrorCustom("登录账号已存在!")
                elif type == '1':
                    raise PubErrorCustom("手机号已存在!")
                elif type == '2':
                    raise PubErrorCustom("邮箱已存在!")

            try:
                user_auth_obj = await self.db.get(UserAuth,userid = pk,type = type)
                user_auth_obj.account = account
                await self.db.update(user_auth_obj)

            except UserAuth.DoesNotExist:

                res = await self.db.execute(
                    UserAuth.select().where(
                        UserAuth.userid == pk,
                        UserAuth.is_password == '0'
                    )
                )
                if not len(res):
                    raise PubErrorCustom("系统异常{}".format(pk))

                await self.db.create(UserAuth, **{
                    "userid": self.pk,
                    "type": type,
                    "account": account,
                    "ticket": res[0].ticket
                })

        if mobile:
            await updUserAuth(account=mobile, type="1",pk=pk)

        if email:
            await updUserAuth(account=email, type="2",pk=pk)

        if login_name:
            await updUserAuth(account=login_name, type="0",pk=pk)

    @Core_connector(**{**UserRules.post(),**{"add_after_handler":add_after_handler}})
    async def post(self,*args,**kwargs):
        return {"data":self.pk}

    @Core_connector(**{**UserRules.put(),**{"upd_before_handler":upd_before_handler}})
    async def put(self,*args,**kwargs):
        pass

    @Core_connector(isTransaction=False)
    async def get(self, pk=None):

        return await user_query(
                        self=self,
                        query= User.select(User).where(User.role_type == '0'),
                        isMobile = True,
                        isEmail  = True,
                        isLoginName = True,
                        isBranch= True,
                        isUserRole=True
                    )

    @Core_connector(**UserRules.delete())
    async def delete(self,*args,**kwargs):
        pass

@route(None,id=True)
class branch(BaseHandler):

    """
    部门管理
    """

    async def upd_before_handler(self,**kwargs):

        logger.info("pk=>{},parent_branch_id=>{}".format(kwargs.get("pk"),self.data.get("parent_branch_id")))
        if str(kwargs.get("pk")) == str(self.data.get("parent_branch_id")):
            self.data["parent_branch_id"] = 0


    @Core_connector(**BranchRules.post())
    async def post(self,*args,**kwargs):
        return {"data":self.pk}

    @Core_connector(**{**BranchRules.put(),**{"upd_before_handler":upd_before_handler}})
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

        self.data['role_id'] = pk
        return await user_query(
                        self=self,
                        query= User.select(User).where(User.role_type == '0'),
                        isMobile = True,
                        isEmail  = True,
                        isBranch=True
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

            if await self.db.count(
                UserLinkRole.select().where(
                    UserLinkRole.role_id == role_id,
                    UserLinkRole.userid == item
                )
            ) <= 0:
                await self.db.create(UserLinkRole,**{
                    "role_id" : role_id,
                    "userid": item
                })

    @Core_connector()
    async def delete(self,pk=None):
        await self.db.execute(
            UserLinkRole.delete().where(
                UserLinkRole.role_id == pk,
                UserLinkRole.userid << self.data.get("ids")
            )
        )

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

@route(None,id=True)
class merchant(BaseHandler):

    """
    租户管理
    """

    async def add_before_handler(self,**kwargs):

        account = self.data.get("account",None)
        password = self.data.get("password","e10adc3949ba59abbe56e057f20f883e")
        merchant_name = self.data.get("merchant_name",None)

        user_obj = await self.db.create(User, **{
            "role_type": "1",
            "name": "{}_admin".format(merchant_name)
        })

        await self.db.create(UserAuth, **{
            "userid": user_obj.userid,
            "type": '0',
            "account": account,
            "ticket": password
        })

        self.data['userid'] = user_obj.userid

    @Core_connector(**{**MerchantRules.post(),**{"add_before_handler":add_before_handler}})
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