
from apps.base import BaseHandler
from utils.decorator.connector import Core_connector
from utils.exceptions import PubErrorCustom
from models.public import AttachMentGroup
from playhouse.shortcuts import model_to_dict


class attachmentgroup(BaseHandler):

    """
    素材分组
    """

    @Core_connector(isPasswd=None)
    async def post(self,pk=None):

        if not self.data.get("name",None):
            raise PubErrorCustom("名称是空!")

        group = await self.db.create(AttachMentGroup,name=self.data.get("name"))

        res = model_to_dict(group)
        caches = [
            {
                "table":"attachmentgroup",
                "key":res['id'],
                "value":res
            }
        ]

        return {
            "caches":caches
        }


    @Core_connector(isPasswd=None)
    async def get(self, pk):
        print(pk)
        # if not self.data.get("name",None):
        #     raise PubErrorCustom("名称是空!")
        #
        # await self.db.create(AttachMentGroup,name=self.data.get("name"))

        return None