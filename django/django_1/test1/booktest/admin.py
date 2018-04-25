from django.contrib import admin
from models import *

#admin.site.register(BookInfo)
admin.site.register(HeroInfo)
# Register your models here.

#class HeroInfoInline(admin.StackedInline):
class HeroInfoInline(admin.TabularInline):
    model=HeroInfo
    extra = 3



class BookInfoAdmin(admin.ModelAdmin):
    list_display = ['id','btitle','bpub_date']
    list_filter = ['btitle']
    search_fields = ['btitle']
    inlines = [HeroInfoInline]


admin.site.register(BookInfo,BookInfoAdmin)
