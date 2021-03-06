
import json
from loguru import logger

from utils.decorator.utils.ticket import ConnectorTicket
from utils.decorator.utils.params import ConnectorParams
from utils.decorator.utils.platform import ConnectorPlatForm

from utils.decorator.utils.save.base import ConnectorFuncsSaveBase
from utils.decorator.utils.delete.base import ConnectorFuncsDeleteBase
from utils.decorator.utils.get.base import ConnectorFuncsGetBase

async def request_before_func_run(**kwargs):

    connector_app = kwargs.get("connector_app")

    logger.info("\n请求IP：{}\n请求方法{}=>{}\n".format(
        connector_app.request.remote_ip,
        connector_app.request.method,
        connector_app.request.uri,
    ))

    await ConnectorTicket(**kwargs).run()
    await ConnectorPlatForm(**kwargs).run()
    await ConnectorParams(**kwargs).run()

    logger.info("\n请求的数据: {}".format(
        json.dumps(connector_app.data,indent=4) if hasattr(connector_app,'data') else None)
    )

async def run_before_func_run(**kwargs):

    connector = kwargs.get("connector")
    connector_app = kwargs.get("connector_app")
    args = kwargs.get("args")

    if len(args) and args[0]:
        pk = args[0]
    else:
        pk = None

    kwargs.setdefault("pk",pk)

    if connector.robot:
        if connector_app.request.method in ['POST','PUT']:
            if connector.add_before_handler:
                await connector.add_before_handler(connector_app,**kwargs)
            if connector.upd_before_handler:
                await connector.upd_before_handler(connector_app,**kwargs)
            await ConnectorFuncsSaveBase(**kwargs).run()
            if connector.add_after_handler:
                await connector.add_after_handler(connector_app,**kwargs)
            if connector.upd_after_handler:
                await connector.upd_after_handler(connector_app,**kwargs)
        elif connector_app.request.method == 'DELETE':
            await ConnectorFuncsDeleteBase(**kwargs).run()
        elif connector_app.request.method == 'GET':
            if connector.get_before_hander:
                await connector.get_before_hander(connector_app,**kwargs)
            return await ConnectorFuncsGetBase(**kwargs).run()
