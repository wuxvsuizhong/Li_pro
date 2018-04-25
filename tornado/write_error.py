#coding:utf-8
import tornado.web
import tornado.ioloop
import tornado.httpserver

from tornado.options import define,options
from tornado.web import RequestHandler

tornado.options.define('port',type=int,default=8000,help="server port")




class IndesHandler(RequestHandler):
    def get(self):
        err_code=self.get_argument('err_code',None)
        err_content=self.get_argument('content')
        err_title=self.get_argument('title')
        
        print (err_code)

        if err_code:
            slef.send_error(err_code,content=err_content,title=err_title)
        else:
            self.write("主页")
        
    def write_error(self,err_code,**kwargs):
        self.write(u"<h1>出错了，error</h1>")
        self.write(u"<p>错误名:%s</p>" % kwargs['title'])
        self.write(u"<p>详情:%s</p>" % kwargs['content'])
        
def main():
    tornado.options.parse_command_line()
    app=tornado.web.Application([
        (r'/',IndesHandler),
    ],debug=True)
    http_server=tornado.httpserver.HTTPServer(app)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.current().start()

if __name__ == '__main__':
    main()
