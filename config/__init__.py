
import os

common=dict(
    gzip = 'on',
    debug = False,
    basedir = os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    port = 8888
)

mysql=dict(
	host = 'localhost',
	port = 3306,
	user = 'root',
    name = "baseshop",
	password = '123456',
    min_connections=2,
    max_connections=10,
    charset='utf8'
)

redis=dict(
    host='localhost',
    port=6379,
    password="123456",
    db = 2,
    minsize = 5,
    maxsize = 20,
    encoding = 'utf8'
)

config_insert=dict(
	common = common,
	mysql = mysql,
	redis = redis
)