#coding:utf-8


from django.db import models

# Create your models here.

#自定义模型类的管理器
class BookInfoManager(models.Manager):
    def get_queryset(self):
        return super(BookInfoManager,self).get_queryset().filter(isdelete=False)
    def create(self,btitle,bpub_date): #快捷创建对象之--1.在自定义管理器中实现创建对象方法
        #b=BookInfo()
        b=self.model()
        b.btitle=btitle
        b.bpub_date=bpub_date
        b.bread=0
        b.bcomment=0
        b.isdelete=False  
        return b



class BookInfo(models.Model):
    btitle=models.CharField(max_length=20)
    bpub_date=models.DateTimeField(db_column='pub_date')
    bread = models.IntegerField(default=0)
    bcomment = models.IntegerField(null=False)
    isdelete = models.BooleanField(default=False)
    class Meta:
        db_table='bookinfo'
        #ordering=['id']
    books1=models.Manager()#指定第一个自定义的管理器
    books2=BookInfoManager()#指定第二个自定义的管理器

    @classmethod    #快捷创建对象之---1.创建类方法(__init__方法已经被Model使用，这里使用不了)
    def create(cls,btitle,bpub_date):
        b=BookInfo()
        b.btitle=btitle
        b.bpub_date=bpub_date
        b.bread=0
        b.bcomment=0
        b.isdelete=False
        return b

    

class HeroInfo(models.Model):
    hname=models.CharField(max_length=10)
    hgender=models.BooleanField(default=True)
    hcontent=models.CharField(max_length=1000)
    isdelete=models.BooleanField(default=False)
    book=models.ForeignKey(BookInfo)



class AreaInfo(models.Model):
    atitle=models.CharField(max_length=20)
    aParent=models.ForeignKey('self',null=True,blank=True)
