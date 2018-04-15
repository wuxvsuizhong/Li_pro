#coding:utf-8
import tornado.web
from tornado.web import RequestHandler
from session import Session

class BaseHandler(RequestHandler):
    """
    handler基类
    """
    def prepare(self):
        self.xsrf_token
        #pass

    def write_error(self,status_code,**kwargs):
        pass

    def set_default_headers(self):
        self.set_header("Content-Type","application/json; charset=UTF-8")

    def initialize(self):
        pass

    def on_finish(self):
        print('on_finish')        

    @property
    def db(self):
        return self.application.db

    @property
    def redis(self):
        return self.application.redis

    def get_current_user(self):
        self.session=Session(self)
        return self.session.data

    def check_args(self,**kwargs):
        """检验入参是否可以为空,一旦存在有参数不能为空但是却没有获取到参数，那么立即返回空字典
            如果成功，返回参数的键值对
        """
        arg_dic={}
        for key,maynull in kwargs.items():
            ret=self.get_argument(key,default='')
            if not ret:
                if maynull:
                    continue;
                else:
                    return {}

            arg_dic[each]=ret

        return arg_dic


class StaticFileHandler(tornado.web.StaticFileHandler):
    def __init__(self,*args,**kwargs):
        super(StaticFileHandler,self).__init__(*args,**kwargs)
        self.xsrf_token
