



from models.public import AttachMentGroup,AttachMent,Menu
from apps.web.public.forms import AttachMentGroupForm,AttachMentForm,MenuForm
from apps.web.public.serializers import AttachMentGroupSerializer,AttachMentSerializer,MenuSerializer

class AttachMentGroupRules:

    @staticmethod
    def post():
        return dict(
            robot={
                "pk_key": "id",
                "attachmentgroup" : {
                    "form_class": AttachMentGroupForm,
                    "model_class": AttachMentGroup
                }
            }
        )

    @staticmethod
    def put():
        return dict(
            robot={
                "pk_key":"id",
                "attachmentgroup": {
                    "form_class": AttachMentGroupForm,
                    "model_class": AttachMentGroup,
                    "father":True
                }
            }
        )

    @staticmethod
    def delete():
        return dict(
            robot={
                "pk_key": "id",
                "attachmentgroup": {
                    "model_class": AttachMentGroup
                }
            }
        )

    @staticmethod
    def get():
        return dict(
            isTransaction=False,
            robot={
                "pk_key": "id",
                "attachmentgroup": {
                    "model_class": AttachMentGroup,
                    "page":True,
                    "serializers":AttachMentGroupSerializer,
                    "query_params":[
                        {
                            "key":"userid",
                            "value":"user.userid",
                            "data_src":"data_pool",
                            "pool":"self"
                        },
                        {
                            "key": "type",
                            "value": "data.type",
                            "data_src": "data_pool",
                            "pool": "self"
                        },
                    ],
                }
            }
        )

class AttachMentRules:

    @staticmethod
    def post():
        return dict(
            robot={
                "pk_key": "id",
                "attachment" : {
                    "form_class": AttachMentForm,
                    "model_class": AttachMent
                }
            }
        )

    @staticmethod
    def put():
        return dict(
            robot={
                "pk_key":"id",
                "attachment": {
                    "form_class": AttachMentForm,
                    "model_class": AttachMent,
                    "father":True
                }
            }
        )

    @staticmethod
    def delete():
        return dict(
            robot={
                "pk_key": "id",
                "attachment": {
                    "model_class": AttachMent
                }
            }
        )

    @staticmethod
    def get():
        return dict(
            isTransaction=False,
            robot={
                "pk_key": "id",
                "attachment": {
                    "model_class": AttachMent,
                    "page":True,
                    "serializers":AttachMentSerializer,
                    "query_params":[
                        {
                            "key":"userid",
                            "value":"user.userid",
                            "data_src":"data_pool",
                            "pool":"self"
                        },
                        {
                            "key": "grouid",
                            "value": "data.grouid",
                            "data_src": "data_pool",
                            "pool": "self",
                            "default":0
                        },
                        {
                            "key": "type",
                            "value": "data.type",
                            "data_src": "data_pool",
                            "pool": "self"
                        },
                    ],
                }
            }
        )

class MenuRules:

    @staticmethod
    def post():
        return dict(
            robot={
                "pk_key": "id",
                "menu" : {
                    "form_class": MenuForm,
                    "model_class": Menu
                }
            }
        )

    @staticmethod
    def put():
        return dict(
            robot={
                "pk_key":"id",
                "menu": {
                    "form_class": MenuForm,
                    "model_class": Menu,
                    "father":True
                }
            }
        )

    @staticmethod
    def delete():
        return dict(
            robot={
                "pk_key": "id",
                "menu": {
                    "model_class": Menu
                }
            }
        )

    @staticmethod
    def get():
        return dict(
            isTransaction=False,
            robot={
                "pk_key": "id",
                "menu": {
                    "model_class": Menu,
                    "page":True,
                    "serializers":MenuSerializer,
                    "sort": Menu.sort,
                    "query_params":[
                        {
                            "key": "parent_id",
                            "value": "data.parent_id",
                            "data_src": "data_pool",
                            "pool": "self",
                            "default":0
                        },
                        {
                            "key": "type",
                            "value": "data.type",
                            "data_src": "data_pool",
                            "pool": "self"
                        },
                    ],
                }
            }
        )