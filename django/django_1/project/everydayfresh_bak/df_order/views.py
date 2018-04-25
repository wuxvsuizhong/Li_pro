#coding:utf-8

from django.shortcuts import render
from django.http import JsonResponse,HttpResponseRedirect
from models import *
from datetime import datetime
from df_cart.models import Cart
from df_goods.models import GoodsInfo
from df_user.models import UserInfo
from django.db.models import Max
from df_user.user_decorator import logindec


def place_order(request):
    choosestr = request.GET['choosestr']
    # print(request.GET)
    buyway = request.GET.get("buyway", '')
    print(choosestr)
    if (choosestr == ''):
        return
    goods_list = choosestr.strip().split(',')
    lenght = len(goods_list)
    for i in range(lenght):
        goods_list[i] = int(goods_list[i])
    userid = int(request.session.get('user_id'))

    #[{},{}]
    try:
        userinfo = UserInfo.objects.get(pk=userid)
    except Exception as e:
        print(e.message)

    recaddr = userinfo.uaddress
    uname = userinfo.uname
    uphone = userinfo.uphone
    #根据选中的商品查询购物车
    list = Cart.objects.filter(cuser=userid, cgoods__in=goods_list)
    lenght = len(list)
    listinfo = []
    for i in range(lenght):
        print('each'+str(list[i].cgoods_id))
        # 查询货物单价,数量,名称
        goodsitem = GoodsInfo.objects.get(pk=list[i].cgoods_id)
        print(goodsitem)
        price = goodsitem.gprice
        gtitle = goodsitem.gtitle
        gpic = goodsitem.gpic
        gunit = goodsitem.gunit
        count = list[i].cgoods_count;
        listinfo.append({'gtitle':gtitle,'gprice':price,'count':count,'gpic':gpic,'gunit':gunit,'gid':goodsitem.id})

    context = {'recaddr':recaddr,'uname':uname,'uphone':uphone,
               'listinfo':listinfo,'kit_name':'提交订单','buyway':buyway}
    return render(request,'df_order/place_order.html',context)


# Create your views here.
def create_order(request):
    print('place_order')
    choosestr = request.GET.get("choosestr",'')
    print(choosestr)
    if(choosestr == ''):
        return JsonResponse({'ok':0})
    goods_list = choosestr.strip().split(',')
    total = float(request.GET.get("total",'0.00'))
    recvaddr = request.GET.get("recvaddr","")
    transfee = float(request.GET.get('transfee',"0.00"))
    userid = int(request.session.get('user_id'))

    #查询已有的订单号
    maxno = None;
    try:
        maxno=Order.objects.aggregate(Max('id'))
        if maxno["id__max"] is None:
            maxno=0
        else:
            maxno = maxno["id__max"]
    except Exception as e:
        print(e.message)

    print('maxno:' + str(maxno))

    #保存订单主要信息
    order = Order()
    order.owner_id = userid
    order.ototal = total
    order.oispay = True
    order.orecaddr = recvaddr
    order.orderno = str(maxno+1).rjust(15,'0')
    order.otransfee = transfee
    order.order_date = "%s"%(datetime.now().strftime("%Y%m%d%H%M%S"))
    order.save()

    print('goods_list'+str(goods_list))
    cart_clearlist=[]
    length = len(goods_list)
    #保存订单详详情
    for i in range(length):
        try:
            item = OrderItem()
            item.goodstype_id = int(goods_list[i])
            itemgoods = Cart.objects.get(cuser=userid,cgoods_id=goods_list[i])
            cart_clearlist.append(itemgoods.id)
            itemcount = itemgoods.cgoods_count
            goodsinfo = GoodsInfo.objects.get(pk=goods_list[i])
            itemprice = goodsinfo.gprice
            item.goodscount = itemcount
            item.sum = itemcount*itemprice
            item.partof_id = order.id
            item.save()
        except Exception as e:
            print(e.message)
            continue

    #保存完信息后清除购物车里的条目
    for i in range(length):
        try:
            item=Cart.objects.get(pk=cart_clearlist[i])
            item.delete()
        except Exception as e:
            print(e.message)
            continue
    #

    return JsonResponse({'ok':1})

# 处理立即下单
@logindec
def buynow(request, goodsid, count):
    #入参 商品id,数量
    user = request.session.get('user_id', '')
    uname = request.session.get('uname','')
    if user != '':
        user = int(user)
    else:
        return JsonResponse()
    #获取运费
    # transfee = request.GET.get('transfee',0)

    #查询出商品价格
    goodsinfo = GoodsInfo.objects.get(pk=goodsid)
    gprice = goodsinfo.gprice
    gpic = goodsinfo.gpic
    gtitle = goodsinfo.gtitle
    gunit = goodsinfo.gunit


    #查询出用户收货地址,电话号码
    userinfo = UserInfo.objects.get(pk=user)
    ushou = userinfo.ushou
    uphone = userinfo.uphone

    order = Order();
    # order.owner = user
    maxno = Order.objects.aggregate(Max('id'))
    # order.orderno = maxno+1
    # order.order_date = '%s'%(datetime.now().strftime("%Y%m%d%H%M%S"))
    # order.ototal = gprice*count
    # order.oispay = False
    # order.otransfee = 0
    listinfo = [{"gid":goodsid,"gpic":gpic,"gtitle":gtitle,"gunit":gunit,"count":count,"gprice":gprice}]
    print(str(listinfo))



    context = {'recaddr':ushou,'uphone':uphone,'uname':uname,
               'listinfo':listinfo }

    return render(request, 'df_order/place_order.html',context)