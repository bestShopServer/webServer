
import json

from loguru import logger

from utils.decorator.utils.base import ConnectorFuncsBase
from utils.exceptions import PubErrorCustom,InnerErrorCustom

from models.shop import ShopSetting

class ConnectorPlatForm(ConnectorFuncsBase):

    async def run(self):
        """
        平台处理
        """

        print(self.connector_app.request.uri.split("/")[3])
        if self.connector_app.request.uri.split("/")[3] == 'app':

            Platform = self.connector_app.request.headers.get_list("Platform")
            Appid = self.connector_app.request.headers.get_list("Appid")

            logger.info("\n请求平台：{}\nAppid：{}\n".format(
                Platform,
                Appid,
            ))

            try:
                self.connector_app.shopsetting = await self.connector_app.db.get(ShopSetting, platform=Platform,appid=Appid)
            except ShopSetting.DoesNotExist:
                raise PubErrorCustom("无效的商户!")

            self.connector_app.shopsetting.setting_data = json.loads(self.connector_app.shopsetting.setting_data)


