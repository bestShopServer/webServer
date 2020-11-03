
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
    role_name = serializers.CharField()

class UserRoleLinkSerializer(serializers.Serializer):

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
    user_role_link = serializers.SerializerMethodField()
    user_branch_link = serializers.SerializerMethodField()

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

    def get_user_role_link(self,obj):
        if hasattr(obj,"user_role_link") and obj.user_role_link:
            return UserRoleLinkSerializer(obj.user_role_link,many=False).data
        else:
            return None

    def get_user_branch_link(self,obj):

        if hasattr(obj,"user_branch_link") and obj.user_branch_link:
            return UserBranchLinkSerializer(obj.user_branch_link,many=False).data
        else:
            return None