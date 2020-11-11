

from apps.web.merchant.forms import \
    BranchFrom,UserRole1Form,UserRole1ForPutForm,\
        MenuLinkMerchantSettingPutForm,MenuLinkMerchantSettingPostForm,\
            MerchantPostForm,MerchantPutForm,User0PostForm,User0PutForm

from models.user import \
    Branch,UserLinkBranch,UserRole,UserLinkRole,\
        MenuLinkMerchantSetting,Merchant,User,UserAuth

from apps.web.merchant.serializers import \
    UserRoleSerializer,UserRoleForMenuSerializer,\
        MenuLinkMerchantSettingSerializer,MerchantSerializer

class BranchRules:

    @staticmethod
    def post():
        return dict(
            robot={
                "pk_key": "branch_id",
                "branch" : {
                    "form_class": BranchFrom,
                    "model_class": Branch,
                    "father": True,
                }
            }
        )

    @staticmethod
    def put():
        return dict(
            robot={
                "pk_key": "branch_id",
                "branch" : {
                    "form_class": BranchFrom,
                    "model_class": Branch,
                    "father": True,
                }
            }
        )

    @staticmethod
    def delete():
        return dict(
            robot={
                "pk_key": "branch_id",
                "branch": {
                    "model_class": Branch,
                    "child": {
                        "userlinkbranch": {
                            "model_class": UserLinkBranch,
                        }
                    }
                }
            }
        )

class UserRoleRules:

    @staticmethod
    def post():
        return dict(
            robot={
                "pk_key": "role_id",
                "role" : {
                    "form_class": UserRole1Form,
                    "model_class": UserRole,
                    "father": True
                }
            }
        )

    @staticmethod
    def put():
        return dict(
            robot={
                "pk_key": "role_id",
                "role" : {
                    "form_class": UserRole1ForPutForm,
                    "model_class": UserRole,
                    "father": True
                }
            }
        )

    @staticmethod
    def delete():
        return dict(
            robot={
                "pk_key": "role_id",
                "role": {
                    "model_class": UserRole,
                    "child": {
                        "userlinkrole": {
                            "model_class": UserLinkRole,
                        }
                    }
                }
            }
        )

    @staticmethod
    def get():
        return dict(
            isTransaction=False,
            robot={
                "pk_key": "role_id",
                "role": {
                    "model_class": UserRole,
                    "serializers":UserRoleSerializer,
                    "page": True
                }
            }
        )

class UserRoleForMenuRules:

    @staticmethod
    def get():
        return dict(
            isTransaction=False,
            robot={
                "pk_key": "role_id",
                "role": {
                    "model_class": UserRole,
                    "serializers":UserRoleForMenuSerializer
                }
            }
        )

class UserRoleLinkRules:

    @staticmethod
    def delete():
        return dict(
            robot={
                "pk_key": "id",
                "userlinkrole": {
                    "model_class": UserLinkRole
                }
            }
        )

class MenuLinkMerchantSettingRules:

    @staticmethod
    def post():
        return dict(
            robot={
                "pk_key": "id",
                "menulinkmerchantsetting" : {
                    "form_class": MenuLinkMerchantSettingPostForm,
                    "model_class": MenuLinkMerchantSetting,
                    "father": True
                }
            }
        )

    @staticmethod
    def put():
        return dict(
            robot={
                "pk_key": "id",
                "menulinkmerchantsetting" : {
                    "form_class": MenuLinkMerchantSettingPutForm,
                    "model_class": MenuLinkMerchantSetting,
                    "father": True
                }
            }
        )

    @staticmethod
    def delete():
        return dict(
            robot={
                "pk_key": "id",
                "menulinkmerchantsetting": {
                    "model_class": MenuLinkMerchantSetting
                }
            }
        )

    @staticmethod
    def get():
        return dict(
            isTransaction=False,
            robot={
                "pk_key": "id",
                "menulinkmerchantsetting": {
                    "model_class": MenuLinkMerchantSetting,
                    "serializers":MenuLinkMerchantSettingSerializer
                }
            }
        )

class MerchantRules:

    @staticmethod
    def post():
        return dict(
            robot={
                "pk_key": "merchant_id",
                "merchant" : {
                    "form_class": MerchantPostForm,
                    "model_class": Merchant,
                    "father": True
                }
            }
        )

    @staticmethod
    def put():
        return dict(
            robot={
                "pk_key": "merchant_id",
                "merchant" : {
                    "form_class": MerchantPutForm,
                    "model_class": Merchant,
                    "father": True
                }
            }
        )

    @staticmethod
    def delete():
        return dict(
            robot={
                "pk_key": "merchant_id",
                "merchant": {
                    "model_class": Merchant
                }
            }
        )

    @staticmethod
    def get():
        return dict(
            isTransaction=False,
            robot={
                "pk_key": "merchant_id",
                "merchant": {
                    "model_class": Merchant,
                    "serializers":MerchantSerializer
                }
            }
        )

class UserRules:

    @staticmethod
    def post():
        return dict(
            robot={
                "pk_key": "userid",
                "user" : {
                    "form_class": User0PostForm,
                    "model_class": User,
                    "father": True,
                    "child_form_link": {
                        "userlinkrole":"roles",
                        "userlinkbranch":"branchs"
                    },
                    "child": {
                        "userlinkrole": {
                            "model_class": UserLinkRole,
                            "data_pool": {
                                "instance": {
                                    "userid": "userid"
                                }
                            }
                        },
                        "userlinkbranch": {
                            "model_class": UserLinkBranch,
                            "data_pool": {
                                "instance": {
                                    "userid": "userid"
                                }
                            }
                        }
                    }
                }
            }
        )

    @staticmethod
    def put():
        return dict(
            robot={
                "pk_key": "userid",
                "user": {
                    "form_class": User0PutForm,
                    "model_class": User,
                    "father": True,
                    "child_form_link": {
                        "userlinkrole": "roles",
                        "userlinkbranch": "branchs"
                    },
                    "child": {
                        "userlinkrole": {
                            "model_class": UserLinkRole,
                            "data_pool": {
                                "instance": {
                                    "userid": "userid"
                                }
                            }
                        },
                        "userlinkbranch": {
                            "model_class": UserLinkBranch,
                            "data_pool": {
                                "instance": {
                                    "userid": "userid"
                                }
                            }
                        },
                    }
                }
            }
        )

    @staticmethod
    def delete():
        return dict(
            robot={
                "pk_key": "userid",
                "user": {
                    "model_class": User,
                    "child": {
                        "userlinkrole": {
                            "model_class": UserLinkRole,
                        },
                        "userlinkbranch": {
                            "model_class": UserLinkBranch,
                        },
                        "userauth": {
                            "model_class": UserAuth,
                        }
                    }
                }
            }
        )