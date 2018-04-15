import tornado.web
import tornado.ioloop
import tornado.httpserver
from tornado.options import options,define

from tornado.web import RequestHandler


tornado.options.define("port",type=int,default=8000,help="server port")



html='<form action="upload" enctype="multipart/form-data" method="post"> \
<input type="file" name="pic"> \
<input type="submit" value="upload"> \
</form>'

class IndexHandler(RequestHandler):
    def get(self):
        self.write(html)

    
    def post(self):
        print self.request.headers
        filename=self.request.files['pic'][0]['filename']
        data=self.request.files['pic'][0]['body']
        with open(filename,'wb') as f:
            f.write(data)






if __name__=='__main__':
    tornado.options.parse_command_line()
    app=tornado.web.Application(
    [
        (r'/',IndexHandler),
        (r'/upload',IndexHandler),
    ],
    debug=True)
    http_server=tornado.httpserver.HTTPServer(app)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.current().start()

