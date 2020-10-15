
import hashlib,random,string,time,requests,xmltodict,json
from decimal import Decimal
from loguru import logger
from utils.exceptions import PubErrorCustom

from models.order import Order

class ShopCartBase(object):

    def __init__(self,**kwargs):

        self.app = kwargs.get("app")

class PayBase(object):

    def __init__(self,**kwargs):

        self.app = kwargs.get("app")
        self.trade = kwargs.get("trade")

    async def run(self):

        if self.trade['paytype'] == '0':

            if self.trade['method'] == 'create':
                return await PayForWechat(
                    app=self.app,
                    trade=self.trade
                ).request()
            else:
                return await PayForWechat(
                    app=self.app,
                    trade=self.trade
                ).callback()
        else:
            raise PubErrorCustom("暂不提供此支付方式!")

class PayForWechat(object):

    def __init__(self,**kwargs):

        self.createUrl = "https://api.mch.weixin.qq.com/pay/unifiedorder"
        self.app = kwargs.get("app")
        self.trade = kwargs.get("trade")

    def hashdata(self,data,key):

        res = self.sortKeyStringForDict(data,key)
        return hashlib.md5(res.encode('utf-8')).hexdigest().upper()

    def sortKeyStringForDict(self,data,key):
        strJoin = ""
        for item in sorted({k: v for k, v in data.items() if v != ""}):
            if item == 'sign':
                continue
            strJoin += "{}={}&".format(str(item), str(data[item]))
        strJoin += "key={}".format(key)
        return strJoin

    async def request(self):

        data={}

        data['appid'] = self.trade['appid']
        data['mch_id'] = self.trade['mch_id']
        data['nonce_str'] = ''.join(random.sample(string.ascii_letters  + string.digits, 30))
        data['body'] = "商城系统-购买商品"
        data['out_trade_no'] = self.trade['out_trade_no']
        data['total_fee'] = self.trade['total_fee']
        data['spbill_create_ip'] = self.trade['spbill_create_ip']
        data['notify_url'] = self.app.settings['callback_url_for_wechat']
        data['trade_type'] = 'JSAPI'
        data['openid'] = self.trade['openid']
        data['sign_type'] = 'MD5'

        data['sign'] = self.hashdata(data,self.trade['pay_key'])

        param = {'root': data}
        xml = xmltodict.unparse(param)

        res = requests.request(method="POST",data=xml.encode('utf-8'),url=self.createUrl,headers={'Content-Type': 'text/xml'})

        xmlmsg = xmltodict.parse(res.content.decode('utf-8'))

        if xmlmsg['xml']['return_code'] == 'SUCCESS':

            sign = self.hashdata(xmlmsg['xml'], self.trade['pay_key'])

            if sign != xmlmsg['xml']['sign']:
                raise PubErrorCustom("非法操作！")

            prepay_id = xmlmsg['xml']['prepay_id']
            timeStamp = str(int(time.time()))

            data = {
                "appId": "",
                "nonceStr": data['nonce_str'],
                "package": "prepay_id=" + prepay_id,
                "signType": 'MD5',
                "timeStamp": timeStamp
            }
            data['paySign']=self.hashdata(data, self.trade['pay_key'])

            data["orderid"] = self.trade['out_trade_no']

            return data
        else:
            raise PubErrorCustom(xmlmsg['xml']['return_msg'])

    async def callback(self):

        # msg = request.body.decode('utf-8')
        xmlmsg = xmltodict.parse(self.trade['callback_msg'])

        return_code = xmlmsg['xml']['return_code']

        logger.info("腾讯支付回调数据:\n\t",xmlmsg['xml'])

        if return_code == 'SUCCESS':

            sign = self.hashdata(xmlmsg['xml'], self.trade['pay_key'])
            if sign != xmlmsg['xml']['sign']:
                logger.error(sign)
                raise Exception("非法操作！")

            if  xmlmsg['xml']['result_code'] == 'SUCCESS':
                out_trade_no = xmlmsg['xml']['out_trade_no']
                total_fee = xmlmsg['xml']['total_fee']

                total_fee = Decimal(str(total_fee))

                try:
                    order = await self.app.db.get(Order, orderid=out_trade_no)
                except Order.DoesNotExist:
                    raise PubErrorCustom("订单{}不存在!".format(out_trade_no))

                if order.pay_amount * 100 != total_fee:
                    raise Exception("金额不一致")

                if order.status=='1':
                    logger.error("订单已处理!")
                    raise Exception("订单已处理!")

                order.trade_no = xmlmsg['xml']['transaction_id']
                order.status='1'

                await self.app.db.update(order)
            else:
                raise Exception("error")
        else:
            raise Exception("error")