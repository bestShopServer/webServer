




import hashlib,random,string,time,requests,xmltodict,json



callback_msg="""
<xml><appid><![CDATA[wx2c4649a77ef8edcd]]></appid>
<bank_type><![CDATA[OTHERS]]></bank_type>
<cash_fee><![CDATA[1]]></cash_fee>
<fee_type><![CDATA[CNY]]></fee_type>
<is_subscribe><![CDATA[N]]></is_subscribe>
<mch_id><![CDATA[1514182671]]></mch_id>
<nonce_str><![CDATA[2PN3m0aLtM1biHwXAEpOc8egdCTW7j]]></nonce_str>
<openid><![CDATA[oiNsJ4wjYFteG97U3mUK9cXEIMkw]]></openid>
<out_trade_no><![CDATA[HG20201020230049001]]></out_trade_no>
<result_code><![CDATA[SUCCESS]]></result_code>
<return_code><![CDATA[SUCCESS]]></return_code>
<sign><![CDATA[A77C9EEAD39243F67A92849B9ED9A267]]></sign>
<time_end><![CDATA[20201020230115]]></time_end>
<total_fee>1</total_fee>
<trade_type><![CDATA[JSAPI]]></trade_type>
<transaction_id><![CDATA[4200000727202010206346505563]]></transaction_id>
</xml>
"""

xmlmsg = xmltodict.parse(callback_msg)

print(xmlmsg)
print(xmlmsg['xml'])