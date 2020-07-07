
import json
from testBase import TestUnitBase


class SkuGroupTest(TestUnitBase):

    def __init__(self):
        super().__init__()

        self.pk = None

        self.api_url = "/goods/goodscategorystyle"

    def post(self):

        self.pk = self.request_handler(
            method="POST",
            url=self.api_url,
            data={"typecode": "ST1001", "type": 1}
        )['data']
        print("{}添加成功!".format(self.pk))

    def put(self):
        self.pk = self.request_handler(
            method="PUT",
            url="{}/{}".format(self.api_url,self.pk),
            data={
                "group_name":"测试分组3"
            }
        )['data']
        print("{}修改成功!".format(self.pk))

    def delete(self):
        self.request_handler(
            method="DELETE",
            url="{}/{}".format(self.api_url,self.pk)
        )
        print("{}删除成功!".format(self.pk))

    def get(self):
        response = self.request_handler(
            method="GET",
            url="{}/{}".format(self.api_url,self.pk) if self.pk else self.api_url
        )['data']
        print("查询数据==>{}".format(json.dumps(response,ensure_ascii=False)))


if __name__ == '__main__':

    s = SkuGroupTest()
    # s.pk = 6
    s.post()
