#coding:utf-8
from models import *
from django.shortcuts import render,redirect
from django.http import HttpResponseRedirect,JsonResponse
from df_user.user_decorator import logindec
from django.db.models import Sum,F
# Create your views here.

@logindec
def show_cart(request):
    kit_name='购物车'
    uname = request.session.get('uname','')
    user_id = request.session.get('user_id','')
    if(user_id == ''):
        return;
    user_bought = Cart.objects.filter(cuser_id=int(user_id))

    boughtlist=[]
    totalcount=0
    if len(user_bought) > 0:
        for each in user_bought:#查询商品信息
            # print(each.cgoods.gtitle)
            goodsinfo = GoodsInfo.objects.get(pk=each.cgoods_id)
            boughtlist.append({'goodsinfo':goodsinfo,'count':each.cgoods_count,'id':each.id})
            totalcount=totalcount+1

    # print(boughtlist)
    print('totalcount:'+str(totalcount))
    context = {'kit_name':kit_name,'uname':uname,'boughtlist':boughtlist,'totalcount':totalcount}
    return render(request,'df_cart/cart.html',context)

def add_goods(request,goods_type,num):
    add2cart(request,goods_type,num)
    if request.is_ajax():
        return
    else:
        return redirect('/cart/')

def add2cart(request,goods_type,num):
    cuser = int(request.session.get('user_id', ''))
    num = int(num)
    # 查找当前用户是否已经购买过传递的商品的类型

    cart_bought = Cart.objects.filter(cuser_id=cuser, cgoods_id=goods_type)
    if (len(cart_bought) > 0):
        cart_bought = cart_bought[0]
        cart_bought.cgoods_count = cart_bought.cgoods_count + num
    else:
        cart_bought = Cart()
        cart_bought.cuser_id = cuser
        cart_bought.cgoods_id = goods_type
        cart_bought.cgoods_count = num
    cart_bought.save()

def addone(request,goods_type):
    print('addone')
    add2cart(request,goods_type,1)

def get_count(request):
    print('get_count view')
    user_id = int(request.session.get('user_id',''))
    if user_id == '':
        return JsonResponse()
    count = Cart.objects.filter(cuser_id=user_id).aggregate(Sum('cgoods_count'))
    countnum = count["cgoods_count__sum"]
    if countnum is None :
        countnum = 0
    print(countnum)
    return JsonResponse({'count':countnum})

def change_count(request,type,num):
    cuser = int(request.session.get('user_id',''))
    type = int(type)
    num = int(num)
    cart=Cart.objects.get(cgoods=type,cuser=cuser)
    cart.cuser_id = cuser
    cart.cgoods_id = type
    cart.cgoods_count = num
    cart.save()
    return JsonResponse({'ret':'ok'})

def delete_goods(request,id):
    cuser = int(request.session.get('user_id', ''))
    try:
        item = Cart.objects.get(cgoods=id,cuser=cuser)
        item.delete()
        return JsonResponse({'data':1})
    except Exception as e:
        print(e.message)
        return JsonResponse({'data':0})
