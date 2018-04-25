from django.contrib import admin
from models import TypeInfo,GoodsInfo

class TypeInfoAdmin(admin.ModelAdmin):
    list_display=['id','ttitle']

class GoodsInfoAdmin(admin.ModelAdmin):
    list_display=['id','gtitle','gpic','gprice','gunit','gbrief','gtype']

# Register your models here.
admin.site.register(TypeInfo,TypeInfoAdmin)
admin.site.register(GoodsInfo,GoodsInfoAdmin)
