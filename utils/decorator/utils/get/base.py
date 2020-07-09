
import copy
from utils.exceptions import PubErrorCustom
from utils.decorator.utils.base import ConnectorFuncsBase

class ConnectorFuncsGetBase(ConnectorFuncsBase):

    def __init__(self,**kwargs):

        super().__init__(**kwargs)

        self.robot = copy.deepcopy(self.connector.robot)

        self.pk_key = self.robot.pop("pk_key")

        if not self.pk_key:
            raise PubErrorCustom("pk_key是空!")

    async def run(self):
        return await self.get()

    def filter(self,model_class,query,query_param):

        if query_param['data_src'] == 'data_pool':
            if query_param['pool'] == 'self':
                value = self.value_recursion(self.connector_app, query_param['value'].split("."))
                if value:
                    query = query.where(getattr(model_class, query_param['key']) == value)
                elif not value and  query_param.get("default",None) != None:
                    query = query.where(getattr(model_class, query_param['key']) == query_param.get("default", None))

        return query

    async def get(self):

        for key,value in self.robot.items():

            model_class = value["model_class"]

            query = model_class.select()

            pk_key = value.get("pk_key") if value.get("pk_key") else self.pk_key

            if self.pk:
                query = query.where(getattr(model_class,pk_key) == self.pk)

            for item in value['query_params']:
                query = self.filter(model_class,query,item)

            if value.get("sort",None):
                query = query.order_by(value.get("sort",None))
            else:
                query = query.order_by(model_class.createtime.desc())

            count = 0
            if value.get("page"):
                count = len(await self.connector_app.db.execute(query))
                query = query.paginate(self.connector_app.data['page'], self.connector_app.data['size'])

            resposne = await self.connector_app.db.execute(query)

            if value.get("child_form_link"):
                for cKey, cValue in value.get("child_form_link").items():
                    child = value['child'][cKey]
                    cModelClass = child['model_class']
                    cPkKey = child.get("pk_key") if child.get("pk_key") else self.pk_key

                    for item in resposne:
                        setattr(item,cValue,
                                    await self.connector_app.db.execute(
                                        cModelClass.select().where(getattr(cModelClass, cPkKey) == getattr(item, pk_key))
                                    )
                                )

            print(resposne)
            data = value['serializers'](resposne, many=True).data

            if self.pk:
                if data and len(data):
                    data = data[0]
                else:
                    data = {}

            return {
                "data": data,
                "count": count
            }
