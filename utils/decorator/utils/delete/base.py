
import copy
from utils.exceptions import PubErrorCustom
from utils.decorator.utils.base import ConnectorFuncsBase

class ConnectorFuncsDeleteBase(ConnectorFuncsBase):

    def __init__(self,**kwargs):

        super().__init__(**kwargs)

        self.robot = copy.deepcopy(self.connector.robot)

        self.pk_key = self.robot.pop("pk_key")

        if not self.pk_key:
            raise PubErrorCustom("pk_key是空!")

    async def run(self):
        if self.connector_app.request.method == 'DELETE':
            await self.delete()

    async def delete_inner_handler(self,**kwargs):

        robot_table = kwargs.get("robot_table")
        model_class = robot_table['model_class']
        pk_key = robot_table.get("pk_key") if robot_table.get("pk_key") else self.pk_key

        if self.pk:
            await self.connector_app.db.execute(model_class.delete(). \
                where(
                    getattr(model_class, pk_key) == self.pk)
                )
        else:
            await self.connector_app.db.execute(model_class.delete(). \
                where(
                    getattr(model_class, pk_key) << self.connector_app.data.get("ids"))
                )

    async def recursion(self,robot):

        if robot:

            for key, value in robot.items():

                await self.delete_inner_handler(
                    robot_table=value
                )
                await self.recursion(robot=value.get("child",None))

    async def delete(self):

        if not self.pk and not self.connector_app.data.get("ids"):
            raise PubErrorCustom("请选择数据!")

        if self.connector.del_before_handler:
            await self.connector.del_before_handler(\
                self.connector_app, self.pk if self.pk else self.connector_app.data.get("ids"))

        if self.connector_app.data.get("ids"):

            if not self.connector.is_del_batch:
                raise PubErrorCustom("此接口不支持批量删除!")

            if not isinstance(self.connector_app.data.get("ids"), list):
                raise PubErrorCustom("批量删除数据格式有误!")

        await self.recursion(self.robot)
