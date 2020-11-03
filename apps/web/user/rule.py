

from apps.web.user.forms import BranchFrom,UserRole0Form,UserRole0ForPutForm
from models.user import Branch,UserLinkBranch,UserRole,UserLinkRole

from apps.web.user.serializers import UserRoleSerializer,UserRoleForMenuSerializer

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
                    # "child_form_link": {
                    #     "userlinkbranch":"user_link_branch"
                    # },
                    # "child": {
                    #     "userlinkbranch": {
                    #         "model_class": UserLinkBranch,
                    #         "data_pool": {
                    #             "instance": {
                    #                 "userid": "userid",
                    #                 "branch_id": "branch_id"
                    #             }
                    #         }
                    #     },
                    # }
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
                    # "child_form_link": {
                    #     "userlinkbranch":"user_link_branch"
                    # },
                    # "child": {
                    #     "userlinkbranch": {
                    #         "model_class": UserLinkBranch,
                    #         "data_pool": {
                    #             "instance": {
                    #                 "userid": "userid",
                    #                 "branch_id": "branch_id"
                    #             }
                    #         }
                    #     },
                    # }
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

    # @staticmethod
    # def get():
    #     return dict(
    #         isTransaction=False,
    #         robot={
    #             "pk_key": "branch_id",
    #             "branch": {
    #                 "model_class": Branch,
    #                 "serializers":BranchSerializer,
    #                 "page": True,
    #                 "query_params":[
    #                     {
    #                         "key":"branch_name",
    #                         "value":"data.branch_name",
    #                         "data_src":"data_pool",
    #                         "pool":"self"
    #                     },
    #                     {
    #                         "key":"status",
    #                         "value": "data.status",
    #                         "data_src":"data_pool",
    #                         "pool":"self"
    #                     }
    #                 ]
    #             }
    #         }
    #     )

class UserRoleRules:

    @staticmethod
    def post():
        return dict(
            robot={
                "pk_key": "role_id",
                "role" : {
                    "form_class": UserRole0Form,
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
                    "form_class": UserRole0ForPutForm,
                    "model_class": UserRole,
                    "father": True,
                    "child_form_link": {
                        "userlinkrole":"user_link_role"
                    },
                    "child": {
                        "userlinkrole": {
                            "model_class": UserLinkRole,
                            "data_pool": {
                                "instance": {
                                    "userid": "userid",
                                    "branch_id": "branch_id"
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