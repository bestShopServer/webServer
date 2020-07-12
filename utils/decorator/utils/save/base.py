
import json,copy
from utils.exceptions import PubErrorCustom
from loguru import logger
from utils.decorator.utils.base import ConnectorFuncsBase

class ConnectorFuncsSaveBase(ConnectorFuncsBase):

    def __init__(self,**kwargs):

        super().__init__(**kwargs)

        self.robot = copy.deepcopy(self.connector.robot)

        self.pk_key = self.robot.pop("pk_key")

        if not self.pk_key:
            raise PubErrorCustom("pk_key是空!")

        self.delete_by_put = None
        self.add_link_by_post_or_put = None

        self.count = 0

    def model_map(self,**kwargs):

        """
        数据map
        :param kwargs:
        :return:
        """

        robot_table_value = kwargs.get("robot_table")
        robot_table_value['instance_data'] = None
        robot_table_value['auto_increment_key'] = self.get_model_auto_increment_key(robot_table_value['model_class'])

        fields = [ k for k in robot_table_value['model_class']._meta.fields ]

        form_data = robot_table_value.get("form_data")

        child_form_link = robot_table_value.get("child_form_link",None)

        data_pool = robot_table_value.get("data_pool",None)

        new_data = {}

        if not form_data:
            return None

        if data_pool:

            if data_pool.get("self",None):
                for key,value in data_pool.get("self",None).items():
                    if key in fields:
                        new_data[key] = self.value_recursion(self.connector_app,value.split("."))

            if data_pool.get("instance",None):
                for key, value in data_pool.get("instance", None).items():
                    if key in fields:
                        new_data[key] = self.value_recursion(robot_table_value.get("last",None)['instance'],value.split("."))

            if data_pool.get("custom",None):
                for key, value in data_pool.get("custom", None).items():
                    if key in fields:
                        new_data[key] = value(
                            connector=self.connector,
                            robot_table_value=robot_table_value,
                            form = form_data
                        )

        for key in fields:

            if robot_table_value['auto_increment_key'] == key and self.connector_app.request.method == 'POST':
                continue

            if not new_data.get(key, None):
                if form_data and form_data.get(key, None):
                    new_data[key] = form_data.get(key) if not isinstance(form_data.get(key),list) else json.dumps(form_data.get(key))

        robot_table_value['instance_data'] = new_data

        if child_form_link and isinstance(child_form_link,dict):
            for key,value in child_form_link.items():
                if isinstance(form_data[value],list):
                    child_tmp = copy.deepcopy(robot_table_value['child'][key])
                    robot_table_value['child'][key] = []
                    for item in form_data[value]:
                        robot_table_value['child'][key].append({**{
                            "form_data":item
                        },**child_tmp})
                elif isinstance(form_data[value],dict):
                    robot_table_value['child'][key]['form_data'] = item
                else:
                    robot_table_value['child'][key]['form_data'] = None

    def delete_by_put_handler(self,**kwargs):

        robot_table = kwargs.get("robot_table")
        res = kwargs.get("res")

        pk_key = robot_table.get("pk_key") if robot_table.get("pk_key") else self.pk_key
        model_class = robot_table["model_class"]
        auto_increment_key = robot_table['auto_increment_key']

        if not robot_table.get("father", None):
            if not self.delete_by_put:
                self.delete_by_put = {
                    self.get_model_table_name(model_class): {
                        "model_class": model_class,
                        "pk_key": pk_key,
                        "no": []
                    }
                }
            elif not self.delete_by_put.get(self.get_model_table_name(model_class)):
                self.delete_by_put[self.get_model_table_name(model_class)] = {
                    "model_class": model_class,
                    "pk_key": pk_key,
                    "no": []
                }

            self.delete_by_put[self.get_model_table_name(model_class)]['no'].append(getattr(res, auto_increment_key))

    def add_link_by_post_or_put_hander(self,**kwargs):

        res = kwargs.get("res")
        robot_table = kwargs.get("robot_table")
        auto_increment_key = robot_table['auto_increment_key']

        last_ids_key = robot_table.get("last_ids_key", None)

        if last_ids_key:

            last_ids_level = int(robot_table.get("last_ids_level", 1))

            model_class_tmp = None
            logger.info(robot_table)
            logger.info(last_ids_level)
            for i in range(last_ids_level):
                model_class_tmp = robot_table.get("last",None)

            if model_class_tmp:

                instance = model_class_tmp['instance']

                if not isinstance(getattr(instance, last_ids_key), list):
                    setattr(instance, last_ids_key,
                            json.loads(
                                getattr(instance, last_ids_key)
                            ).append(getattr(res, auto_increment_key))
                            )
                else:
                    setattr(instance, last_ids_key,
                            [getattr(res, auto_increment_key)]
                            )

                if not self.add_link_by_post_or_put:
                    self.add_link_by_post_or_put = {
                        self.get_model_table_name(model_class_tmp['model_class']): {
                            "instance": instance,
                            "ids_key": [
                                {
                                    last_ids_key:[]
                                }
                            ]
                        }
                    }
                elif not self.add_link_by_post_or_put.get(self.get_model_table_name(model_class_tmp['model_class'])):
                    self.add_link_by_post_or_put[self.get_model_table_name(model_class_tmp['model_class'])] = {
                        "instance": instance,
                        "ids_key": [
                                {
                                    last_ids_key:[]
                                }
                            ]
                    }
                elif last_ids_key not in self.add_link_by_post_or_put.get(self.get_model_table_name(model_class_tmp['model_class']))[
                    'ids_key']:
                    self.add_link_by_post_or_put[self.get_model_table_name(model_class_tmp['model_class'])]['instance'] = instance
                    self.add_link_by_post_or_put[self.get_model_table_name(model_class_tmp['model_class'])]['ids_key'].append(
                                {last_ids_key:[]})

                self.add_link_by_post_or_put.get(self.get_model_table_name(model_class_tmp['model_class']))[
                    'ids_key'][last_ids_key].append(getattr(robot_table['instance'],auto_increment_key))


    def filter(self,query_param):

        if query_param['data_src'] == 'data_pool':
            if query_param['pool'] == 'self':
                return self.value_recursion(self.connector_app, query_param['value'].split("."))

    async def check_unique(self,**kwargs):
        robot_table = kwargs.get("robot_table")
        model_class = robot_table["model_class"]

        if robot_table.get("unique",None):
            try:
                await self.connector_app.db.get(model_class,
                        **{
                            item['key'] :  self.filter(item)\
                            for item in robot_table.get("unique")
                        }
                    )
                raise PubErrorCustom("已存在!")
            except model_class.DoesNotExist:
                pass

    async def _save(self,**kwargs):

        robot_table = kwargs.get("robot_table")

        instance_data = robot_table['instance_data']
        model_class = robot_table["model_class"]
        auto_increment_key = robot_table['auto_increment_key']
        sort_key  = robot_table.get("sort_key",None)

        if not instance_data:
            return None

        self.count += 1

        if sort_key:
            instance_data.setdefault(sort_key, self.count)

        if self.connector_app.request.method == 'PUT':

            if instance_data.get(auto_increment_key, None):
                res = model_class(**instance_data)
                await self.connector_app.db.update(res)
            else:
                await self.check_unique(robot_table=robot_table)
                res = await self.connector_app.db.create(model_class, **instance_data)
            self.delete_by_put_handler(robot_table=robot_table, res=res)
        else:
            await self.check_unique(robot_table=robot_table)
            res =  await self.connector_app.db.create(model_class, **instance_data)

        self.add_link_by_post_or_put_hander(robot_table=robot_table,res=res)
        return res

    async def form_robot_hander(self,robot_table):

        form_class = robot_table.get("form_class",None)

        if form_class:

            form_data = robot_table['form_data'] if robot_table.get("form_data",None) else self.connector_app.data

            if hasattr(self.connector_app, "user") and form_data:
                form_data['userid'] = self.connector_app.user['userid']

            if robot_table.get("father",None) and self.connector_app.request.method == 'PUT':
                form_data[self.get_model_auto_increment_key(robot_table['model_class'])] = self.pk

            form_obj = form_class(**form_data)

            if not form_obj.validate():
                error_str = ""
                for field in form_obj.errors:
                    error_str += "{}; ".format(form_obj.errors[field][0])
                raise PubErrorCustom(error_str)

            robot_table['form_data'] = form_obj.data

    async def robot_recursion_inner(self,robot_table,last):

        robot_table['last'] = last
        await self.form_robot_hander(robot_table=robot_table)
        self.model_map(robot_table=robot_table)
        robot_table['instance'] = await self._save(robot_table=robot_table)
        if robot_table.get("father") and self.pk_key:
            self.connector_app.pk = getattr(robot_table['instance'],self.pk_key)
        await self.robot_recursion(robot=robot_table.get("child", None), last=robot_table)

    async def robot_recursion(self,robot,last=None):

        if robot:

            for key,value in robot.items():
                if isinstance(value,list):
                    for item in value:
                        await self.robot_recursion_inner(robot_table=item,last=last)
                elif isinstance(value,dict):
                    await self.robot_recursion_inner(robot_table=value, last=last)

    async def after_hander(self):

        if self.delete_by_put:
            for key,value in self.delete_by_put.items():
                await self.connector_app.db.execute(
                    value['model_class'].delete().\
                        where (
                            getattr(value['model_class'], value['pk_key']) == self.pk,
                            getattr(value['model_class'], self.get_model_auto_increment_key(value['model_class'])).not_in(value['no'])
                        )
                )

        logger.info(self.add_link_by_post_or_put)
        if self.add_link_by_post_or_put:
            for key,value in self.add_link_by_post_or_put.items():
                instance = value['instance']
                for idKey,idValue in value['ids_key'].items():
                    setattr(instance,idKey,json.dumps(idValue))
                await self.connector_app.db.update(instance)

    async def save(self):

        await self.robot_recursion(self.robot)
        await self.after_hander()

    async def run(self):
        await self.save()

