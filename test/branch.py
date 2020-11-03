





import json
from testBase import TestUnitBase


class Branch(TestUnitBase):

    def __init__(self):
        super().__init__()

        self.pk = None

        self.api_url = "/user/menu_for_role"

    def post(self):
        self.pk = self.request_handler(
            method="POST",
            url=self.api_url,
            data={
                "parent_branch_id":1,
                "branch_name": "测试部门2",
            }
        )['data']
        print("{}添加成功!".format(self.pk))

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

    s = Branch()
    # s.post()
    # s.delete()
    # # s.pk = 1
    s.get()
