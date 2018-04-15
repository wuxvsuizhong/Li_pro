#coding:utf-8

from django.shortcuts import render,redirect
from models import *
from df_order.models import *
from df_goods.models import GoodsInfo
from hashlib import sha1
from django.http import JsonResponse,HttpResponse,HttpResponseRedirect
from user_decorator import logindec
from django.core.paginator import Paginator


# Create your views here.
def register(request):
    return render(request,'df_user/register.html')

def register_handle(request):
    post = request.POST
    uname = post.get('user_name')
    upwd = post.get('pwd')
    upwd2 = post.get('cpwd')
    uemail = post.get('email')
    #两次判断密码
    if upwd != upwd2:#密码不符合，跳转到新注册页面
        return redirect('/user/register/')
    #加密
    s1 = sha1()
    s1.update(upwd)
    upwd3 = s1.hexdigest()

    #创建对象
    user = UserInfo()
    user.uname = uname
    user.upwd = upwd3
    user.uemail = uemail

    user.save()
    #注册完成后返回登录页面
    return render(request,'df_user/login.html')

#检验用户名是否存在
def register_exist(request):
    uname = request.GET['uname']
    count = UserInfo.objects.filter(uname=uname).count()
    return JsonResponse({'count':count})

def user_login(request):
    # isremmber = request.session.get('')
    context = {'title':'用户登录','uname_error':0,'pwd_error':0}
    return render(request,'df_user/login.html',context)

@logindec
def show_user_info(request):
    user_id = request.session.get('user_id')
    uname = request.session.get('uname')
    # print('user_info:uname--'+uname)
    seluserinfo = UserInfo.objects.filter(pk=int(user_id))[0]
    #获最近浏览数据
    goods_list = request.COOKIES.get('clicked_goods','').split(',')
    # print('goods_list'+str(goods_list))
    clicked_list = []
    if goods_list !=['']:
        for eachid in goods_list:
            clicked_list.append(GoodsInfo.objects.get(pk=int(eachid)))

    context = {'user_info':seluserinfo,'title':'用户中心','uname':uname,'clicked_list':clicked_list}
    return render(request,'df_user/user_center_info.html',context)

def login_handle(request):
    post = request.POST
    uname = post.get('username')
    upwd = post.get('pwd')
    isremember = post.get('remeber')

    print(uname)
    print(upwd)
    print('isremember:'+str(isremember))

    if(uname == '' or upwd == ''):
        return redirect('/user/login/')

    #很据用户明查询
    user = UserInfo.objects.filter(uname=uname)#filter返回的是一个列表
    print(user)
    if(len(user)) == 1:
        # 加密
        s1 = sha1()
        s1.update(upwd)
        upwd2 = s1.hexdigest()
        url = request.COOKIES.get('url','/')
        print('-'*10+url)

        if user[0].upwd == upwd2:#匹配用户密码成功

            red = HttpResponseRedirect(url)

            if isremember == 'on':#用户是否勾选记住密码
                red.set_cookie('uname',uname)
            else:
                red.set_cookie('uname','',-1)

            request.session['user_id'] = user[0].id
            request.session['uname'] = user[0].uname
            request.session.set_expiry(0)
            return red
        else:#密码错误
            context={'title':'用户登录','pwd_error':1,'uname_error':0}
            return render(request,'df_user/login.html',context)
    else:#用户不存在
        print('point 1111')
        context={'title':'用户登录','uname_error':1,'pwd_error':0}
        return render(request,'df_user/login.html',context)

def user_logout(request):
    request.session.flush()
    return redirect('/')

@logindec
def user_center_order(request,pageno):
    user = request.session.get('user_id','')
    uname = request.session.get('uname','')
    # pageno = request.GET.get('pageno','1')
    if (pageno is None) or (pageno == ''):
        pageno='1'
    pageno = int(pageno)
    pagelist=[]
    if user != '':
        user = int(user)
    #查询订单主要信息-条件：用户id
    try:
        pagelist = Order.objects.filter(owner=user).order_by('-id')
    except Exception as e:
        print(e.message)
        return

    pages=Paginator(pagelist,3)

    # 总共有几页
    totalpage = pages.page_range
    page = pages.page(pageno)
    if pageno > totalpage:
        curpage = totalpage
    # 当前页码
    curpage = pageno


    orderlist = []
    for each in page:
        order_id = each.id
        ordertime = each.order_date

        print(ordertime)
        orderno = each.orderno
        ispay = each.oispay
        total = each.ototal
        print('each:'+str(each.id))

        #查询订单所属的商品条目
        items=None
        try:
            # items = each.orderitem_set().order_by('-id')
            items = OrderItem.objects.filter(partof_id=order_id)
        except Exception as e:
            print(e.message)

        print('items:'+str(items))
        itemlist = []
        for each in items:
            goodsinfo = GoodsInfo.objects.get(pk=each.goodstype_id)
            gpic = goodsinfo.gpic
            gtitle = goodsinfo.gtitle
            gprice = goodsinfo.gprice
            gunit = goodsinfo.gunit
            goodscount = each.goodscount
            sum = each.sum
            itemlist.append({"gpic":gpic,"gtitle":gtitle,"gprice":gprice,
                             "gunit":gunit,"goodscount":goodscount,"sum":sum})

        orderlist.append({"order_id":order_id,"ordertime":ordertime,
                          "orderno":orderno,"ispay":ispay,"total":total,"itemlist":itemlist})

    #{当前页码，总页数，订单列表[{订单id,下单时间，单号，是否支付，总费用，{商品条目}},{}]}
    context = {"curpage":curpage,"totalpage":totalpage,"orderlist":orderlist,"kit_name":"用户中心","uname":uname}
    print(context)
    return render(request,'df_user/user_center_order.html/',context)

@logindec
def user_center_site(request):
    user = request.session.get('user_id','')
    if user != '':
        user = int(user)
    else:
        return
    userinfo = UserInfo.objects.get(pk=user)
    addr = userinfo.uaddress
    ushou = userinfo.ushou
    uname = userinfo.uname
    uphone = userinfo.uphone
    context={'addr':addr,'uname':uname,'uphone':uphone,'ushou':ushou}

    return render(request,'df_user/user_center_site.html',context)

@logindec
def change_address(request):
    user = request.session.get('user_id', '')
    if user != '':
        user = int(user)
    else:
        return
    userinfo = UserInfo.objects.get(pk=user)
    initushou = userinfo.ushou
    inituaddress = userinfo.uaddress
    inituyoubian = userinfo.uyoubian
    inituphone = userinfo.uphone

    post = request.POST

    ushou = post.get('recname',initushou)
    ushou = initushou if ushou=='' else ushou
    recaddress = post.get('recaddress',inituaddress)
    recaddress = inituaddress if recaddress=='' else recaddress
    youbian = post.get('youbian',inituyoubian)
    youbian = inituyoubian if youbian=='' else youbian
    uphone = post.get('uphone',inituphone)
    uphone = inituphone if uphone=='' else uphone

    userinfo.ushou=ushou
    userinfo.uyoubian = youbian
    userinfo.uaddress = recaddress
    userinfo.uphone = uphone
    userinfo.save()
    return redirect('/index/')
