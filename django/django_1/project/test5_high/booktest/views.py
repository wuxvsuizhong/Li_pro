#coding:utf-8

from django.shortcuts import render
from django.conf import settings
from django.http import HttpResponse,JsonResponse
from models import *
from django.core.paginator import *


# Create your views here.
def index(request):
    # num=int('abc')
    return render(request,'booktest/index.html')

def uploadPic(request):
    return render(request,'booktest/upload.html')

def uploadHandle(request):
    pic=request.FILES['pic1']
    file_name='%s/%s' %(settings.MEDIA_ROOT,pic.name)
    with open(file_name,'w') as data:
        for c in pic.chunks():
            data.write(c)
    #return HttpResponse(file_name)
    return HttpResponse('OK')

#数据分页
def herolist(request,index):
    if index is None:
        index='1'
    list=HeroInfo.objects.all()
    paginator=Paginator(list,5)
    page=paginator.page(int(index))
    context={'page':page}
    return render(request,'booktest/herolist.html',context)

#省市区选择
def area(request):
    return render(request,'booktest/area.html')

def area2(request,Parea):
    p_area=int(Parea)
    if p_area == 0:#没有上级机构,查询省
        data=AreaInfo.objects.filter(aparent__isnull=True)
    else:
        data=[{}]
    list=[]
    for each in data:
        list.append([each.atitle,each.id])
    datas={'data':list}
    return JsonResponse(datas)#直接返回json对象{'data':[[atitle,aparent],[atitle,aparent]]}

def city(request,id):
    citylist = AreaInfo.objects.filter(aparent_id=id)
    list=[]
    for each in citylist:
        list.append([each.atitle,each.id])
    datas={'data':list}
    return JsonResponse(datas)

#自定义编辑器
def HmtlEditor(request,id):
    return render(request,'booktest/editor.html')