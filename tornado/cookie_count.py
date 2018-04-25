#coding:utf-8


from tornado import web,ioloop,httpserver
from tornado.web import RequestHandler,Application
from tornado.options import options,define

options.define('port',type=int,default=8000,help='server port')

class Index(RequestHandler):
    def get(self):
        count=self.get_secure_cookie("page_count")
        if count:
            count=int(count)   
            count += 1
            self.set_secure_cookie("page_count",str(count))
            self.write("访问"+str(count)+"次")
        else:
            self.set_secure_cookie("page_count",'1')
            self.write('OK!')

def main():
    options.parse_command_line()
    settings=dict(
        cookie_secret="EXigJx+bSIKYZxFZaSPXtQjZbFP9C0r2lpA4b8AS+bk=",
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
