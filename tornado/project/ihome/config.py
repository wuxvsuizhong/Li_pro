#coding:utf-8
import os

#tornado.web.Application配置
settings=dict(
    static_path=os.path.join(os.path.dirname(__file__),'static'),
    template_path=os.path.join(os.path.dirname(__file__),'template_path'),
    cookie_secret="9imLUMO9TiSm0pnAXHhWqam4G2UzHkn3nJ5ecFP2tjM=",
    xsrf_cookies=True,
    debug=True,
)

#mysql配置
mysql_options=dict(
    host='localhost',
    database='ihome',
    user='root',
    password='231024'
)

#redis配置
redis_options=dict(
    host='localhost',
    port=6379
)

log_file=os.path.join(os.path.dirname(__file__),"logs/log")
log_level="debug"
