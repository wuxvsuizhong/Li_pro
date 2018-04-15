from tornado import web,ioloop,httpserver
import tornado.options import options,define
from tornado.web import RequestHandler

class Index(RequestHandler):
    def get(self):
        data=dict(
            
        )
        render('house.html',{'data':data})
