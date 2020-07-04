


import json
from testBase import TestUnitBase


class AttachMent(TestUnitBase):

    def __init__(self):
        super().__init__()

        self.pk = None

        self.api_url = "/public/attachmentgroup"

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

    s = AttachMent()
    s.pk = 1
    s.delete()
    # s.delete()
