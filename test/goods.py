
import json
from testBase import TestUnitBase


class SkuGoodsTest(TestUnitBase):

    def __init__(self):
        super().__init__()

        self.pk = None

        self.api_url = "/goods/goods"

    def post(self):

        self.pk = self.request_handler(
            method="POST",
            url=self.api_url,
            data={
                "gd_name":"测试商品1",
                "gd_link_type":[6],
                "gd_status":"0",
                "gd_sort":100,
                "gd_banners": [
                    ["image", "http://139.13.1.33/image/1.png"],
                    ["video", "http://139.13.1.33/video/2.mp4"],
                ],
                "gd_show_price":100,
                "gd_mark_price":101,
                "gd_unit":"件",
                "gd_cost_price":110,
                "gd_stock_tot":300,
                "gd_stock_show":'0',
                "gd_specs_name_default":"",
                "gd_specs_name_default_flag":'1',
                "gd_item_no":"HY001",
                "gd_weight":300,
                "gd_sku_link": [
                    {
                        "skus": [
                            {
                                "group_id": 6,
                                "spec_id": 1
                            }
                        ],
                        "image": "image",
                        "price": 100.00,
                        "stock": 50,
                        "item_no": "HY001",
                        "weight": 100,
                        "cost_price": 120.00
                    }
                ],
                "gd_sell_number":500,
                "gd_fare_mould_id":0,
                "gd_limit_number_by_goods":-1,
                "gd_limit_number_by_order":-1,
                "gd_include_fare1":0,
                "gd_include_fare2":0.0,
                "gd_allow_area_flag":'0',
                "gd_allow_area": [
                    {
                        "province": "110000",
                        "province_name": "北京市"
                    },
                    {
                        "province": "130000",
                        "province_name": "河北省",
                        "city": "130100",
                        "city_name": "石家庄市",
                        "country": "130123",
                        "country_name": "正定县"
                    },
                ],
                "gd_share_title":"分享标题",
                "gd_share_image":"gd_share_image"
            }
        )['data']
        print("{}添加成功!".format(self.pk))

    def get(self):
        response = self.request_handler(
            method="GET",
            url="{}/{}".format(self.api_url,self.pk) if self.pk else self.api_url
        )['data']
        print("查询数据==>{}".format(json.dumps(response,ensure_ascii=False)))

if __name__ == '__main__':

    s = SkuGoodsTest()
    s.get()
