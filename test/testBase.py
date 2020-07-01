
import requests,json

class TestUnitBase(object):

    def __init__(self):
        self.base_url =  "http://localhost:8888/api/v1"
        self.token = None

        self.get_token()

    def url(self,appendurl):

        return "{}{}".format(self.base_url,appendurl)

    def request_handler(self,**kwargs):

        method = kwargs.get("method")
        url = self.url(kwargs.get("url"))
        data = {
            "data":kwargs.get("data",{})
        }
        params = {
            "data":json.dumps(kwargs.get("params",{}))
        }
        headers = {
            "Authorization": self.token
        }

        response = requests.request(
            method=method,
            url=url,
            json=data,
            params=params,
            headers=headers)
        try:
            response = json.loads(response.content.decode('utf-8'))
            if response['code'] != '10000':
                raise Exception(response['msg'])
        except Exception as e:
            raise Exception(str(e))

        return response

    def get_token(self):

        self.token = self.request_handler(
            method="POST",
            url="/sso/login",
            data={
                "loginname": "admin",
                "password": "e10adc3949ba59abbe56e057f20f883e"
            }
        )['data']

