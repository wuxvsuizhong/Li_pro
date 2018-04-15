import tornado.web
import tornado.httpserver
from tornado.options import options,define
import tornado.ioloop
import os
import torndb
from tornado.web import RequestHandler

tornado.options.define('port',type=int,default=8000,help='server port')

current_path=os.path.dirname(__file__)


class Index(RequestHandler):
    def get(self):
        sql="select house_name from houses where house_id='1'"
        text=self.application.db.get(sql)['house_name']
        self.render('new.html',text=text)

def main():
    tornado.options.parse_command_line()
    settings=dict(
        static_path=os.path.join(current_path,'static'),
        template_path=os.path.join(current_path,'template'),
        debug=True
    )

    app=tornado.web.Application([
        (r'/',Index),
    ],**settings)

    app.db=torndb.Connection(
        host='localhost',
        database='TestDB3',
        user='root',
        password='231024',
    )

    server=tornado.httpserver.HTTPServer(app)
    server.listen(options.port)
    tornado.ioloop.IOLoop.current().start()

if __name__=='__main__':
    main()


