

from peewee import *
from models.base import BaseModel

from utils.hash import md5


class User(BaseModel):

    id=BigIntegerField(primary_key=True)

    userid = BigIntegerField(verbose_name="用户ID")
    rolecode=IntegerField(verbose_name="角色代码")

    name = CharField(max_length=120, verbose_name="名称", default='', null=True)
    passwd = CharField(max_length=60,verbose_name='密码',default='')
    pay_passwd = CharField(max_length=60,verbose_name='支付密码',default='')
    addr = CharField(max_length=255, verbose_name="地址", default='', null=True)
    sex = CharField(max_length=10, verbose_name="性别", default='', null=True)

    uuid =  CharField(max_length=60, verbose_name="用户小程序ID/用户账号", default='', null=True)
    mobile = CharField(max_length=60, verbose_name="手机号", default='', null=True)

    pic=CharField(max_length=255,verbose_name="头像地址",default='')

    status = CharField(max_length=1,default='0',verbose_name="状态:0-正常，1-到期,2-冻结",null=True)

    bal = DecimalField(max_digits=18,decimal_places=6,default=0.000,verbose_name="余额")

    shopinfo = TextField(verbose_name="""
                            店铺基础信息
                                wechat:微信小程序数据
                                    appid:微信小程序appid,
                                    secret:微信小程序appkey,
                                    pay_mchid:微信小程序支付商户ID,
                                    pay_key:微信小程序支付key
                                goodscategory_level:分类层级,最多3级
                                shopname:店铺名称
                        """,
                         default="""{"wechat":{"appid":"","secret":"","pay_mchid":"","pay_key":""},"goodscategory_level":0,"shopname":"店铺"}""")

    def save(self, *args, **kwargs):

        if not self.passwd:
            self.passwd = md5('123456')
        if not self.pay_passwd:
            self.pay_passwd = md5('123456')
        return super(User, self).save(*args, **kwargs)


class Role(BaseModel):

    id = AutoField(primary_key=True)
    rolecode =  CharField(max_length=4,default='')
    roletype = CharField(max_length=1,default='0',verbose_name="1-管理员,2-机构,3-商户,4-用户")
    name = CharField(max_length=60,default='')

    """
    1000 - 系统管理员
    1001 - 普通管理员 
    2001 - 机构代理
    3001 - 商户管理员
    3002 - 商户销售
    4001 - 微信用户
    """

    # class Meta:
    #     verbose_name = '角色表'
    #     verbose_name_plural = verbose_name
    #     db_table = 'role'