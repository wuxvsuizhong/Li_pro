#coding:utf-8

import tornado.web
import tornado.ioloop

class IndexHandler(tornado.web.RequestHandler):
    def get(self):
        self.write('hrllo tornado!')



if __name__=='__main__':
    app=tornado.web.Application([('/',IndexHandler)])
    app.listen(8000)
    tornado.ioloop.IOLoop.current().start()

