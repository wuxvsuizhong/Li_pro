#coding:utf-8

import tornado.web
import tornado.httpserver
import tornado.ioloop
import os

from tornado.options import define,options
from tornado.web import RequestHandler,StaticFileHandler


tornado.options.define('port',type=int,default=8000,help='server port')
current_path=os.path.dirname(__file__)
class IndexHandler(RequestHandler):
    def get(self):
        self.write("<h1>静态文件获取</h1>")
        self.write("<img src='/static/image01.jpg' alt='image'>")


if __name__=='__main__':
    tornado.options.parse_command_line()
    app=tornado.web.Application([
        (r'/',IndexHandler),
        (r'/view/image/(.*)$',StaticFileHandler,{"path":os.path.join(current_path,"static")}),
    ],
    static_path=os.path.join(os.path.dirname(__file__),"static"),
    debug=True
    )
    server=tornado.httpserver.HTTPServer(app)
    server.listen(options.port)
    tornado.ioloop.IOLoop.current().start()
