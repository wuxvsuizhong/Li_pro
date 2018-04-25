#coding:utf-8

from django.http import HttpResponseRedirect


def logindec(func):
    def login_func(request,*args,**kwargs):
        if request.session.has_key('user_id'):#判断会话是否有保存用户的id
            # print('dec--uname:'+str(request.session['uname']))
            return func(request,*args,**kwargs)
        else:#没有记录用户id(没登录过）
            red= HttpResponseRedirect('/user/login/')
            red.set_cookie('url',request.get_full_path()) #记录此时用户所在的页面请求
            return red
    return login_func



