

from models.setting import FareRule,FareLinkCity
from apps.web.setting.forms import FareRuleForm
from apps.web.setting.serializers import FareRuleSerializer

class FareRuleRules:

    @staticmethod
    def post():
        return dict(
            robot={
                "pk_key": "fare_rule_id",
                "farerule" : {
                    "form_class": FareRuleForm,
                    "model_class": FareRule,
                    "father": True,
                    "child_form_link":{
                          "farelinkcity":"fare_rule_link_citys"
                    },
                    "child": {
                        "farelinkcity":{
                            "model_class": FareLinkCity,
                            "data_pool": {
                                "instance": {
                                    "userid": "userid",
                                    "fare_rule_id": "fare_rule_id"
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
                "pk_key":"fare_rule_id",
                "farerule": {
                    "form_class": FareRuleForm,
                    "model_class": FareRule,
                    "father":True,
                    "child_form_link": {
                        "farelinkcity": "fare_rule_link_citys"
                    },
                    "child": {
                        "farelinkcity": {
                            "model_class": FareLinkCity,
                            "data_pool": {
                                "instance": {
                                    "userid": "userid",
                                    "fare_rule_id": "fare_rule_id"
                                }
                            }
                        }
                    }
                }
            }
        )

    @staticmethod
    def delete():
        return dict(
            robot={
                "pk_key": "fare_rule_id",
                "farerule": {
                    "model_class": FareRule,
                    "child": {
                        "farelinkcity": {
                            "model_class": FareLinkCity,
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
                "pk_key": "fare_rule_id",
                "farerule": {
                    "model_class": FareRule,
                    "page":True,
                    "serializers":FareRuleSerializer,
                    "query_params":[
                        {
                            "key":"userid",
                            "value":"user.userid",
                            "data_src":"data_pool",
                            "pool":"self"
                        }
                    ],
                    "child_form_link": {
                        "farelinkcity": "fare_rule_link_citys"
                    },
                    "child": {
                        "farelinkcity": {
                            "model_class": FareLinkCity,
                        }
                    }
                }
            }
        )