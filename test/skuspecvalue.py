
import json
from testBase import TestUnitBase


class SkuSpecValueTest(TestUnitBase):

    def __init__(self):
        super().__init__()

        self.pk = None

        self.api_url = "/goods/skuspecvalue"

    def post(self):

        self.pk = self.request_handler(
            method="POST",
            url=self.api_url,
            data={
                "spec_value":"测试值1",
                "group_id":6
            }
        )['data']
        print("{}添加成功!".format(self.pk))

    def put(self):
        self.pk = self.request_handler(
            method="PUT",
            url="{}/{}".format(self.api_url,self.pk),
            data={
                "group_id": 6,
                "spec_value":"测试值3"
            }
        )['data']
        print("{}修改成功!".format(self.pk))

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

    s = SkuSpecValueTest()
    s.pk = 5
    # s.get()
    # s.post()
    s.put()
    # s.delete()
