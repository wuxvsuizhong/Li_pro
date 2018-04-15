#coding:utf-8
import tornado.web
import tornado.ioloop
import os,torndb
from tornado.options import options,define
from tornado.web import RequestHandler

tornado.options.define('port',type=int,default=8000,help='server port')
current_path=os.path.dirname(__file__)

class Index(RequestHandler):
    def get(self):
        sql='select house_name from houses where house_id=%(house_id)s'
        text=self.application.db.get(sql,house_id=1)['house_name']
        self.render('new.html',text=text)

class Application(tornado.web.Application):
    #集成Application类，实现自定义数据库接口
    def __init__(self,*arg,**kwargs):
        handlers=[
            (r'/',Index),
        ]

        settings=dict(
            static_path=os.path.join(current_path,'sttaic'),
            template_path=os.path.join(current_path,'template'),
            debug=True
        )
    
        super(Application,self).__init__(handlers,**settings)

        self.db=torndb.Connection(
            host='localhost',
            database='TestDB3',
            user='root',
            password='231024',
        )

def main():
    tornado.options.parse_command_line()
    app=Application()
    server=tornado.httpserver.HTTPServer(app)
    server.listen(options.port)
    tornado.ioloop.IOLoop.current().start()

if __name__=='__main__':
    main()
