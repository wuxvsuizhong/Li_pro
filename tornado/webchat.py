#coding:utf-8


from tornado import web,ioloop,httpserver
from tornado.options import options,define
import os
from tornado.web import Application,RequestHandler,StaticFileHandler
from tornado.websocket import WebSocketHandler

options.define('port',type=int,default=8000,help='server port')

class ChatHandler(WebSocketHandler):
    users=[]

    def open(self):
        for user in self.users:
            user.write_message("%s上线了"%self.request.remote_ip)
        self.users.append(self)

    def on_message(self,msg):
        for user in self.users:
            user.write_message("%s:%s"%(self.request.remote_ip,msg))
    def on_close(self):
        self.users.remove(self)
        for user in self.users:
            user.write_message("%s下线"%self.request.remote_ip)

class Index(RequestHandler):
    def get(self):
        self.render('webchat.html')
        


def main():
    options.parse_command_line()
    settings=dict(
        template_path=os.path.join(os.path.dirname(__file__),'template'),
        static_path=os.path.join(os.path.dirname(__file__),'static'),
        debug=True
    )
    app=Application([
        (r'/webchat',ChatHandler),
        (r'.',Index)
    ],**settings)

    server=httpserver.HTTPServer(app)
    server.listen(options.port)
    ioloop.IOLoop.current().start()
    
if __name__ == '__main__':
    main()
