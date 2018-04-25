#coding:utf-8
from django.shortcuts import render
from django.http import HttpResponse
from models import *
from django.views.decorators.cache import cache_page
from django.core.cache import cache
from task import *

# Create your views here.

#富文本编辑器（引入第三方）
def TestHtml(request):
    return render(request,'booktest/edtor.html')

def HtmlEditorHandle(request):
    html = request.POST['hcontent']
    test1 = Test1.objects.get(pk=1)
    test1.content = html
    test1.save()
    context={'content':html}
    return render(request,'booktest/showHtmlStr.html',context)

#缓存
@cache_page(60*10)
def cache1(request):
#    return HttpResponse('hellos')
#     return HttpResponse('hellos2')
#     cache.set('key1','value1',600)
    #cache.delete('key1')
    #return render(request, 'booktest/cache1.html')
    cache.clear()
    return HttpResponse('ok')

#全文检索和中文分词
def mysearch(request):
    return render(request,'booktest/mysearch.html')

def celeryTest(request):
    # show()
    show.delay()
    return HttpResponse('ok')