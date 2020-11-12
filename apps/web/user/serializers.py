
import json
from rest_framework import serializers

from utils.time_st import UtilTime

class BranchSerializer(serializers.Serializer):

    branch_id = serializers.IntegerField()

    parent_branch_id = serializers.IntegerField()
    branch_name = serializers.CharField()

    super_man_name = serializers.CharField()
    super_man_phone = serializers.CharField()
    super_man_email = serializers.CharField()

    status = serializers.CharField()
    sort = serializers.IntegerField()

class UserRoleSerializer(serializers.Serializer):

    role_id = serializers.IntegerField()
    role_name = serializers.CharField()

    sort = serializers.IntegerField()
    status = serializers.CharField()

    # menus = serializers.SerializerMethodField()
    #
    # def get_menus(self,obj):
    #
    #     return json.loads(obj.menus)

class UserRoleForMenuSerializer(serializers.Serializer):

    menus = serializers.SerializerMethodField()

    def get_menus(self,obj):

        return json.loads(obj.menus)

class UserAuthByPhoneEmailSerializer(serializers.Serializer):

    account = serializers.CharField()

class UserRoleForNameSerializer(serializers.Serializer):
    role_id = serializers.IntegerField()
    role_name = serializers.CharField()

class UserRoleLinkSerializer(serializers.Serializer):

    id = serializers.IntegerField()
    userrole = serializers.SerializerMethodField()

    def get_userrole(self,obj):
        return UserRoleForNameSerializer(obj.userrole,many=False).data

class UserBranchForNameSerializer(serializers.Serializer):
    branch_id = serializers.IntegerField()
    branch_name = serializers.CharField()

class UserBranchLinkSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    branch = serializers.SerializerMethodField()

    def get_branch(self, obj):
        return UserBranchForNameSerializer(obj.branch, many=False).data

class UserSerializer(serializers.Serializer):

    userid = serializers.IntegerField()
    status = serializers.CharField()
    name = serializers.CharField()
    pic = serializers.CharField()
    memo = serializers.CharField()
    sex = serializers.CharField()

    mobile = serializers.SerializerMethodField()
    email = serializers.SerializerMethodField()
    login_name = serializers.SerializerMethodField()
    userlinkrole = serializers.SerializerMethodField()
    userlinkbranch = serializers.SerializerMethodField()

    def get_mobile(self,obj):
        if hasattr(obj,"mobile") and obj.mobile:
            return UserAuthByPhoneEmailSerializer(obj.mobile,many=False).data
        else:
            return None

    def get_email(self,obj):
        if hasattr(obj,"email") and obj.email:
            return UserAuthByPhoneEmailSerializer(obj.email,many=False).data
        else:
            return None

    def get_login_name(self,obj):
        if hasattr(obj,"login_name") and obj.email:
            return UserAuthByPhoneEmailSerializer(obj.login_name,many=False).data
        else:
            return None

    def get_userlinkrole(self,obj):
        if hasattr(obj,"userlinkrole") and obj.userlinkrole:
            return UserRoleLinkSerializer(obj.userlinkrole,many=True).data
        else:
            return None

    def get_userlinkbranch(self,obj):

        if hasattr(obj,"userlinkbranch") and obj.userlinkbranch:
            return UserBranchLinkSerializer(obj.userlinkbranch,many=True).data
        else:
            return None

class MenuLinkMerchantSettingSerializer(serializers.Serializer):

    id = serializers.IntegerField()
    default = serializers.CharField()
    name = serializers.CharField()
    status = serializers.CharField()
    memo = serializers.CharField()
    menus = serializers.SerializerMethodField()

    def get_menus(self,obj):
        return json.loads(obj.menus)

class MerchantSerializer(serializers.Serializer):

    merchant_id = serializers.IntegerField()
    merchant_name = serializers.CharField()

    sort = serializers.IntegerField()
    memo = serializers.CharField()

    status = serializers.SerializerMethodField()

    account = serializers.SerializerMethodField()

    expire_time = serializers.IntegerField()
    createtime = serializers.IntegerField()

    def get_account(self,obj):
        if obj.user and obj.user.userauth:
            return obj.user.userauth.account
        else:
            return None

    def get_status(self,obj):
        if obj.status =='0':
            if obj.expire_time <= UtilTime().timestamp:
                return '1'
            else:
                return '0'

        return obj.status




class MerchantLinkUserSerializer(serializers.Serializer):

    merchant_id = serializers.SerializerMethodField()
    merchant_name = serializers.SerializerMethodField()
    memo = serializers.SerializerMethodField()
    status = serializers.SerializerMethodField()
    expire_time = serializers.SerializerMethodField()

    def get_merchant_id(self,obj):
        return obj.merchant.merchant_id

    def get_merchant_name(self,obj):
        return obj.merchant.merchant_name

    def get_memo(self,obj):
        return obj.merchant.memo

    def get_status(self,obj):
        return obj.merchant.status

    def get_expire_time(self,obj):
        return obj.merchant.expire_time