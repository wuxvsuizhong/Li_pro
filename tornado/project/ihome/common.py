#coding:utf-8
import logging
def require_logined(f):
    def wrapper(request_handler,*args,**kwargs):
        try:        
            if request_handler.get_current_user():
                f(request_handler,*args,**kwargs)
            else:
                request_handler.write({"ret":"0","msg":"未登录"})
        except Exception as e:
            logging.error(e.message)
            request_handler.write({"ret":"0","msg":"系统错误"})
    return wrapper