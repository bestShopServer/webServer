
import json

from utils.decorator.utils.base import ConnectorFuncsBase

from utils.exceptions import PubErrorCustom

from utils.aes import decrypt

class ConnectorParams(ConnectorFuncsBase):

    async def run(self):
        """
        参数统一处理
        """

        if self.connector.isParams:
            if self.connector_app.request.method in ['POST', 'PUT', 'DELETE']:
                self.connector_app.data = self.connector_app.get_body_argument("data", None)
                if not self.connector_app.data:
                    self.connector_app.data = json.dumps(
                        json.loads(self.connector_app.request.body.decode('utf-8')).get("data", None)) \
                        if self.connector_app.request.body \
                        else '{}'
                if not self.connector_app.data:
                    self.connector_app.data = '{}'
            elif self.connector_app.request.method == 'GET':
                self.connector_app.data = self.connector_app.get_query_argument("data", None)
            else:
                raise PubErrorCustom("拒绝访问!")

            if not self.connector_app.data:
                raise PubErrorCustom("拒绝访问!")

            # 加密处理
            if self.connector.isPasswd:
                if self.connector_app.data != '{}':
                    self.connector_app.data = json.loads(decrypt(self.connector_app.data))
                else:
                    self.connector_app.data = json.loads(self.connector_app.data)
            else:
                self.connector_app.data = json.loads(self.connector_app.data)

            if self.connector_app.request.method == 'GET':
                if self.connector_app.data.get("page"):
                    self.connector_app.data['page'] = int(self.connector_app.data.get("page"))
                else:
                    self.connector_app.data['page'] = 1

                if self.connector_app.data.get("size"):
                    self.connector_app.data['size'] = int(self.connector_app.data.get("size"))
                else:
                    self.connector_app.data['size'] = 10