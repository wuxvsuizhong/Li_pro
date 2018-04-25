#coding:utf-8


import tornado.web
import tornado.ioloop
import tornado.httpserver
import tornado.options

from tornado.options import define,options
from tornado.web import RequestHandler,url

tornado.options.define("port",type=int,default=8000,help="服务器端口")

class IndexHandler(RequestHandler):
    def get(self):
        subject=self.get_query_argument('subject','python')
        #获取get携带的参数（url中的）
        query_args=self.get_query_arguments('q')#获取全部的值
        query_arg=self.get_query_argument('q')#获取单个的值,以出现先后顺序，最终得到的是最后的值
        #获取post提交的参数
        body_args=query.get_body_arguments('b')
        body_arg=query.get_body_argument('b')
        self.write(str(query_args))


if __name__=='__main__':
    tornado.options.parse_command_line()
    app=tornado.web.Application(
    [
        (r'/',IndexHandler),
    ],
    debug=True
    )

    http_server=tornado.httpserver.HTTPServer(app)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.current().start()
                 
