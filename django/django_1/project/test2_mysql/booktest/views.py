#coding:utf-8
from django.shortcuts import render
from models import *
from django.db.models import Max,F,Q

def index(request):
    #list=BookInfo.books1.filter(heroinfo__hcontent__contains='')
    #list=BookInfo.books1.aggregate(Max('bpub_date'))
    #max1=BookInfo.books1.filter(bread__gt=20)
    #max2=BookInfo.books1.filter(bread__gt=F('bcomment'))#bread>bcomment查询
    #list1=BookInfo.books1.filter(pk__lt=4,btitle__contains='天')
    list1=BookInfo.books1.filter(Q(pk__lt=4)|Q(btitle__contains='1'))
    context = {    
    #'list':list,
    #'max1':max1,
    #'max2':max2,
    'list1':list1,
    }
    return render(request,'booktest/index.html',context)


def area(request):
    list1=AreaInfo.objects.get(pk=654300)
    context={'area':list1,}
    return render(request,'booktest/area.html',context)


