#coding:utf-8

from django.shortcuts import render
from models import *
from django.http import HttpResponse
# Create your views here.

def index(request):
    #hero=HeroInfo.objects.get(pk=1)
    #context={'hero':hero}

    list=HeroInfo.objects.filter(isdelete=False)
    context={'list':list}
    return render(request,'booktest/index.html',context)


def show(request,id):
    context={'id':id}
    return render(request,'booktest/show.html',context)

def index2(request):
    return render(request,'booktest/index2.html')

def user1(request):
    context={'uname':'zhww'}
    return render(request,'booktest/user1.html',context)

def user2(request):
    return render(request,'booktest/user2.html')

def htmlTest(request):
    context={'t1':'<h1>123sdf</h1>'}
    return render(request,'booktest/htmlTest.html',context)

def csrf1(request):
    return render(request,'booktest/csrf1.html')

def csrf2(request):
    uname = request.POST['uname']
    return HttpResponse(uname)

def verifyCode(request):
    from PIL import Image,ImageDraw,ImageFont
    import random
    #创建背景色
    bgcolor=(random.randrange(50,100),random.randrange(50,100),0)
    width=100
    height=25
    #创建画布
    image=Image.new('RGB',(width,height),bgcolor)
    #创建画笔
    draw=ImageDraw.Draw(image)
    #构造字体对象
    font=ImageFont.truetype('FreeMono',24)
    #创建文本内容
    text='0123abcdABCD'
    #逐个绘制字符
    texttemp=''
    for i in range(4):
        chartemp=text[random.randrange(0,len(text))]
        texttemp+=chartemp
        draw.text((i*25,0),chartemp,(255,255,255),font)
    #draw.text((0,0),text,(255,255,255),font)
    request.session['code']=texttemp
    #保存生成的文件到内存流
    import cStringIO
    buf=cStringIO.StringIO()
    image.save(buf,'png')
    #将保存的内存流文件输出到客户端

    return HttpResponse(buf.getvalue(),'image/png')

def verifyTest(request):
    return render(request,'booktest/verifyTest1.html')

def verifyTest2(request):
    recCode=request.POST['code1']
    code2=request.session['code']
    if recCode == code2:
        return HttpResponse('OK')
    else:
        return HttpResponse('NO')