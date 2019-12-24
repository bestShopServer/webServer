
from apps.base import BaseHandler
from utils.decorator.connector import Core_connector


class attachmentgroup(BaseHandler):

    """
    素材分组
    """

    @Core_connector(isTicket=False)
    async def post(self, *args, **kwargs):

        return None