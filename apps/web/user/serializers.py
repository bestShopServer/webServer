
import json
from rest_framework import serializers

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
    branch_name = serializers.CharField()

class UserBranchLinkSerializer(serializers.Serializer):
    branch = serializers.SerializerMethodField()

    def get_branch(self, obj):
        return UserBranchForNameSerializer(obj.branch, many=False).data

class UserSerializer(serializers.Serializer):

    userid = serializers.IntegerField()
    status = serializers.CharField()
    name = serializers.CharField()
    pic = serializers.CharField()
    memo = serializers.CharField()

    phone = serializers.SerializerMethodField()
    email = serializers.SerializerMethodField()
    login_name = serializers.SerializerMethodField()
    userlinkrole = serializers.SerializerMethodField()
    userlinkbranch = serializers.SerializerMethodField()

    def get_phone(self,obj):
        if hasattr(obj,"phone") and obj.phone:
            return UserAuthByPhoneEmailSerializer(obj.phone,many=False).data
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

class MerchantSerializer(serializers.Serializer):

    merchant_id = serializers.IntegerField()
    merchant_name = serializers.CharField()

    sort = serializers.IntegerField()
    memo = serializers.CharField()

    status = serializers.CharField()

    expire_time = serializers.IntegerField()
    createtime = serializers.IntegerField()