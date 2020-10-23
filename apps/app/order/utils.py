
import hashlib,random,string,time,requests,xmltodict,json
from decimal import Decimal
from loguru import logger
from utils.exceptions import PubErrorCustom

from utils.time_st import UtilTime
from models.order import Order,OrderRefund
from models.setting import FareRule

class ShopCartBase(object):

    def __init__(self,**kwargs):

        self.app = kwargs.get("app")

class OrderBase(object):

    def __init__(self):
        pass

    def query(self):
        pass

class FareBase(object):

    def __init__(self,**kwargs):

        self.app = kwargs.get("app")
        self.goods = kwargs.get("goods")

    async def fare_cals(self,id=None):

        try:
            obj = await self.app.db.get(FareRule, fare_rule_id=id)
        except FareRule.DoesNotExist:
            logger.info("运费规则{}不存在!".format(id))
            return Decimal('0.0')

        #按重量计费
        if obj.fare_rule_fee_type == '0':
            pass
        #按件计费
        else:
            pass


class PayBase(object):

    def __init__(self,**kwargs):

        self.app = kwargs.get("app")
        self.trade = kwargs.get("trade")

    async def get_base_params(self):

        self.trade['appid'] = "wx2c4649a77ef8edcd"
        self.trade['mch_id'] = "1514182671"
        self.trade['pay_key'] = "15176427685562895401199204202038"

    async def run(self):

        await self.get_base_params()

        if self.trade['paytype'] == '0':

            if self.trade['method'] == 'create':
                return await PayForWechat(
                    app=self.app,
                    trade=self.trade
                ).request()
            elif self.trade['method'] == 'callback':
                return await PayForWechat(
                    app=self.app,
                    trade=self.trade
                ).callback()
            elif self.trade['method'] == 'refund':
                return await PayForWechat(
                    app=self.app,
                    trade=self.trade
                ).refund()
            elif self.trade['method'] == 'refund_callback':
                return await PayForWechat(
                    app=self.app,
                    trade=self.trade
                ).refund_callback()
            else:
                raise PubErrorCustom("method({}) error!".format(self.trade['method']))
        else:
            raise PubErrorCustom("暂不提供此支付方式!")

class PayForWechat(object):

    def __init__(self,**kwargs):

        self.createUrl = "https://api.mch.weixin.qq.com/pay/unifiedorder"
        self.refundUrl = "https://api.mch.weixin.qq.com/secapi/pay/refund"
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
        logger.info(data)
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
                "appId": self.trade['appid'],
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
        logger.info("支付回调数据=>{}".format(self.trade))
        xmlmsg = xmltodict.parse(self.trade['callback_msg'])

        logger.info("回调数据=>{}".format(xmlmsg))
        return_code = xmlmsg['xml']['return_code']

        logger.info(return_code)
        logger.info("腾讯支付回调数据:{}\n\t",xmlmsg['xml'])

        if return_code == 'SUCCESS':

            sign = self.hashdata(xmlmsg['xml'], self.trade['pay_key'])
            if sign != xmlmsg['xml']['sign']:
                logger.error(sign)
                raise Exception("非法操作！")

            if  xmlmsg['xml']['result_code'] == 'SUCCESS':
                out_trade_no = xmlmsg['xml']['out_trade_no']
                total_fee = xmlmsg['xml']['total_fee']

                total_fee = Decimal(str(total_fee))

                order = await self.app.db.execute(Order.select().for_update().where(Order.orderid == out_trade_no))
                if not len(order):
                    raise PubErrorCustom("订单{}不存在!".format(out_trade_no))
                else:
                    order = order[0]

                if order.pay_amount * 100 != total_fee:
                    raise Exception("金额不一致")

                if order.status=='1':
                    logger.error("订单已处理!")
                    raise Exception("订单已处理!")

                order.trade_no = xmlmsg['xml']['transaction_id']
                order.status='1'

                order.status_list = json.dumps(json.loads(order.status_list).append({"status": "1", "time": UtilTime().timestamp}))

                await self.app.db.update(order)
            else:
                raise Exception("error")
        else:
            raise Exception("error")

    async def refund(self):

        data = {}

        data['appid'] = self.trade['appid']
        data['mch_id'] = self.trade['mch_id']
        data['nonce_str'] = ''.join(random.sample(string.ascii_letters + string.digits, 30))
        data['out_trade_no'] = self.trade['out_trade_no']
        data['sign_type'] = 'MD5'
        data['out_refund_no'] = self.trade['out_refund_no']
        data['total_fee'] = self.trade['total_fee']
        data['refund_fee'] = self.trade['refund_fee']
        data['notify_url'] = self.app.settings['refund_callback_url_for_wechat']

        data['sign'] = self.hashdata(data, self.trade['pay_key'])
        logger.info(data)
        param = {'root': data}
        xml = xmltodict.unparse(param)

        res = requests.request(method="POST", data=xml.encode('utf-8'), url=self.refundUrl,
                               headers={'Content-Type': 'text/xml'})

        xmlmsg = xmltodict.parse(res.content.decode('utf-8'))

        if xmlmsg['xml']['return_code'] != 'SUCCESS':
            raise PubErrorCustom(xmlmsg['xml']['return_msg'])


    async def refund_callback(self):

        # msg = request.body.decode('utf-8')
        logger.info("退款回调数据=>{}".format(self.trade))
        xmlmsg = xmltodict.parse(self.trade['callback_msg'])

        logger.info("回调数据=>{}".format(xmlmsg))
        return_code = xmlmsg['xml']['return_code']

        if return_code == 'SUCCESS':

            sign = self.hashdata(xmlmsg['xml'], self.trade['pay_key'])
            if sign != xmlmsg['xml']['sign']:
                logger.error(sign)
                raise Exception("非法操作！")

            if  xmlmsg['xml']['result_code'] == 'SUCCESS':
                out_trade_no = xmlmsg['xml']['out_trade_no']
                refund_fee = xmlmsg['xml']['refund_fee']

                refund_fee = Decimal(str(refund_fee))

                order_refund = await self.app.db.execute(OrderRefund.select().for_update().where(OrderRefund.orderid == out_trade_no))
                if not len(order_refund):
                    raise PubErrorCustom("退款信息{}不存在!".format(out_trade_no))
                else:
                    order_refund = order_refund[0]

                if order_refund.refund_amount * 100 != refund_fee:
                    raise Exception("金额不一致")

                if order_refund.status=='2':
                    logger.error("退款单已处理!")
                    raise Exception("退款单已处理!")

                # order_refund.trade_no = xmlmsg['xml']['transaction_id']
                order_refund.status='2'

                order = await self.app.db.execute(Order.select().for_update().where(Order.orderid == out_trade_no))
                if not len(order):
                    raise PubErrorCustom("订单{}不存在!".format(out_trade_no))
                else:
                    order = order[0]

                order.status = '5'
                order.status_list = json.dumps(json.loads(order.status_list).append({"status": "5", "time": UtilTime().timestamp}))

                await self.app.db.update(order_refund)
                await self.app.db.update(order)
            else:
                raise Exception("error")
        else:
            raise Exception("error")