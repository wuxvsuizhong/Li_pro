#coding:utf-8
import os

from tornado import web,ioloop,httpserver
from tornado.web import RequestHandler,Application
from tornado.options import options,define

options.define('port',type=int,default=9000,help='server port')

class Index(RequestHandler):
    def get(self):
        self.render('img.html')
def main():
    options.parse_command_line()
    settings=dict(
        cookie_secret="EXigJx+bSIKYZxFZaSPXtQjZbFP9C0r2lpA4b8AS+bk=",
        template_path=os.path.join(os.path.dirname(__file__),'template'),
        debug=True
    )
    app=Application([
        (r'/',Index)
    ],**settings)
    server=httpserver.HTTPServer(app)
    server.listen(options.port)
    ioloop.IOLoop.current().start()


if __name__ == '__main__':
    main()
