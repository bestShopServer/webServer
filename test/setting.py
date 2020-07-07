


import json
from testBase import TestUnitBase


class SettingTest(TestUnitBase):

    def __init__(self):
        super().__init__()

        self.pk = None

        self.api_url = "/setting/farerule"

    def post(self):

        self.pk = self.request_handler(
            method="PUT",
            url=self.api_url,
            data={
                "fare_rule_name":"测试规则",
                "fare_rule_fee_type":"1",
                "fare_rule_first_weight":1,
                "fare_rule_first_fee":20,
                "fare_rule_join_weight":30,
                "fare_rule_join_fee":40,
                "fare_rule_link_citys":[
                    {
                        "id":48,
                        "province": "11111",
                        "province_name": "ssssss"
                    },
                    {
                        "id":49,
                        "province": "11111",
                        "province_name": "11111",
                        "city": "130100",
                        "city_name": "11",
                        "country": "130123",
                        "country_name": "正定22县"
                    }
                ]
            }
        )['data']
        print("{}添加成功!".format(self.pk))

    def put(self):

        self.pk = self.request_handler(
            method="PUT",
            url="{}/{}".format(self.api_url,self.pk),
            data={
                "fare_rule_name":"测试规则",
                "fare_rule_fee_type":"1",
                "fare_rule_first_weight":1,
                "fare_rule_first_fee":20,
                "fare_rule_join_weight":30,
                "fare_rule_join_fee":40,
                "fare_rule_link_citys":[
                    {
                        "province": "11111",
                        "province_name": "ssssss"
                    },
                    {
                        "province": "11111",
                        "province_name": "11111",
                        "city": "130100",
                        "city_name": "11",
                        "country": "130123",
                        "country_name": "正定22县"
                    }
                ]
            }
        )['data']
        print("{}添加成功!".format(self.pk))

    def delete(self):
        self.request_handler(
            method="DELETE",
            url="{}/{}".format(self.api_url,self.pk)
        )
        print("{}删除成功!".format(self.pk))

    # def get(self):
    #     response = self.request_handler(
    #         method="GET",
    #         url="{}/{}".format(self.api_url,self.pk) if self.pk else self.api_url
    #     )['data']
    #     print("查询数据==>{}".format(json.dumps(response,ensure_ascii=False)))


if __name__ == '__main__':

    s = SettingTest()
    s.post()
    # s.delete()
