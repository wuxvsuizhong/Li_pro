#coding:utf-8

from django.shortcuts import render,redirect
from django.http import HttpResponseRedirect
from models import *
from django.core.paginator import Paginator


# Create your views here.
def index(request):
    return HttpResponseRedirect('/index/')

def show_index(request):
    uname = request.session.get('uname','')
    typelist = TypeInfo.objects.all()
    type0 = typelist[1].goodsinfo_set.order_by('-id')[0:4]#最新添加的4个
    type01 = typelist[1].goodsinfo_set.order_by('-gclick')[0:3]#点击量最多的3个
    type1 = typelist[5].goodsinfo_set.order_by('-id')[0:4]
    type11 = typelist[5].goodsinfo_set.order_by('-gclick')[0:3]
    context={'type0':type0,'type01':type01,'type1':type1,'type11':type11,'uname':uname}
    return render(request,'df_goods/index.html',context)


def show_list(request,type,orderby,pageno):
    #request后跟得形参分别为产品类型,排序依据,页码
    type = int(type)
    type = TypeInfo.objects.get(pk=type)   #查询某个类型
    news = type.goodsinfo_set.order_by('-id')[0:2]
    uname = request.session.get('uname', '')
    if orderby == '1':#默认按照最新
        goodslist = GoodsInfo.objects.filter(gtype_id=type).order_by('-id')
    elif orderby == '2':#按照点击量
        goodslist = GoodsInfo.objects.filter(gtype_id=type).order_by('-gclick')
    else:
        goodslist = GoodsInfo.objects.filter(gtype_id=type).order_by('gprice')

    pages = Paginator(goodslist,15)
    pagelist = pages.page(int(pageno))
    pagesnum = pages.page_range
    curpage = int(pageno)
    listpath = request.path
    print('listpath:'+listpath)
    context = {'title':type.ttitle,'pagelist':pagelist,'news':news,'pagesnum':pagesnum,
               'curpage':curpage,'orderby':orderby,'uname':uname,'listtype':type.id,'listpath':listpath}
    return render(request,'df_goods/list.html',context)


def show_detail(request,id):
    uname = request.session.get('uname', '')
    goodsdetail = GoodsInfo.objects.get(pk=int(id))
    goodsdetail.gclick = goodsdetail.gclick+1
    goodsdetail.save()
    news = goodsdetail.gtype.goodsinfo_set.order_by('-id')[0:2]
    goodstype = goodsdetail.gtype
    typeid = goodsdetail.gtype_id
    # print('goodstype:'+goodstype.ttitle)
    context = {'goodsdetail':goodsdetail,'news':news,'uname':uname,'goodstype':goodstype,'typeid':typeid}

    #记录点击过的商品
    clicked_goods=request.COOKIES.get('clicked_goods','')
    clicked_id = '%s'% id
    if clicked_goods != '':
        goods_list = clicked_goods.split(',')

        if goods_list.count(clicked_id) != 0:
            goods_list.remove(clicked_id)
        goods_list.insert(0, clicked_id)
        if len(goods_list)>=6:#超过5个的删除队列尾部的数据
            del goods_list[5]
        clicked_goods = ','.join(goods_list)#拼接成字符串
    else:
        clicked_goods=''.join(clicked_id)

    print('clicked_goods'+clicked_goods)

    res = render(request,'df_goods/detail.html',context)
    res.set_cookie('clicked_goods',clicked_goods)


    # return render(request,'df_goods/detail.html',context)

    return res

