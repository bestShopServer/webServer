

class ConnectorFuncsBase(object):

    def __init__(self,**kwargs):

        self.connector = kwargs.get("connector")
        self.connector_app = kwargs.get("connector_app")
        self.args = kwargs.get("args")
        self.kwargs = kwargs.get("kwargs")
        self.pk = kwargs.get("pk")

        self.platform = self.connector_app.request.uri.split("/")[3]

    def get_model_table_name(self,model):
        return model._meta.table_name

    def get_model_auto_increment_key(self,model):

        return model._meta.primary_key.name

    def value_recursion(self, pool, value):

        if value and len(value):

            value_tmp = value.pop(0)

            if isinstance(pool, dict):
                pool_tmp = pool.get(value_tmp,None)
            else:
                pool_tmp = getattr(pool, value_tmp)

            return self.value_recursion(pool_tmp, value)
        else:
            return pool

    # def get_pk_key(self,**kwargs):
    #
    #     model_dict = kwargs.get("model_dict")
    #
    #     pk_key = None
    #
    #     if model_dict.get('pk_key'):
    #         pk_key = model_dict.get('pk_key')
    #     else:
    #         last = model_dict.get('last',None)
    #         while not pk_key:
    #
    #             if not last:
    #                 break
    #
    #             if not last.get("pk_key", None):
    #                 last = last.get("last",None)
    #                 continue
    #             else:
    #                 pk_key = last.get('pk_key')
    #
    #     if not pk_key:
    #         pk_key = self.connector.pk_key
    #
    #     return pk_key