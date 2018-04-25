import tornado.web
import tornado.httpserver
import tornado.ioloop

from tornado.options import options,define
from tornado.web import RequestHandler
import os

options.define('port',type=int,default=8000,help='server port')


class IndexHandler(RequestHandler):
    def get(self):
        self.render('new.html',text="")

    def post(self):
        self.set_header('X-XSS-Protection',0)
        text=self.get_argument('text')
        self.render('new.html',text=text)



def main():
    tornado.options.parse_command_line()
    app=tornado.web.Application([
        (r'/',IndexHandler),
    ],
    debug=True,
    template_path=os.path.join(os.path.dirname(__file__),'template'),
    autoescape=None
    )
    
    server=tornado.httpserver.HTTPServer(app)
    server.listen(options.port)
    tornado.ioloop.IOLoop.current().start()

if __name__ == '__main__':
    main()
