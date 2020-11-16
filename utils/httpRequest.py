
import json
from urllib.parse import urlencode
from loguru import logger
from tornado.httpclient import AsyncHTTPClient,HTTPRequest

from utils.exceptions import PubErrorCustom

async def HttpRequestCustom(**kwargs):

    url = kwargs.get("url")
    method = kwargs.get("method","GET")
    params = kwargs.get("params",None)
    body = kwargs.get("body",None)
    herders = kwargs.get("herders",None)

    logger.info("请求参数:url=>{},method=>{},params=>{},body=>{},herders=>{}"\
                .format(
        url,method,params,body,herders
    ))

    http_client = AsyncHTTPClient()

    if params:
        url = "{}?{}".format(url,urlencode(params))

    if body:
        body = json.dumps(body).encode("utf8")

    try:
        response = await http_client.fetch(HTTPRequest(url=url, method=method,body=body,headers=herders))
    except Exception as e:
        raise PubErrorCustom("Error: %s" % e)
    else:

        if response.code != 200:
            raise PubErrorCustom(response.error)

        response = json.loads(response.body.decode('utf8'))

        logger.info("返回值=>{}".format(response))

        return response