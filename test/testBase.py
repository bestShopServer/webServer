
import requests,json

class TestUnitBase(object):

    def __init__(self):
        self.base_url =  "http://localhost:8888/v1/api/web"
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
                "loginname": "9336578@qq.com",
                "password": "4d974f12b2349c766c913432d32b47c2"
            }
        )['data']

        print(self.token)

if __name__=='__main__':

    s = TestUnitBase()

    print(s.token)