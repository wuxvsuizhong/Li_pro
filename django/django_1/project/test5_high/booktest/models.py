from django.db import models

# Create your models here.
class BookInfo(models.Model):
    btitle = models.CharField(max_length=20)
    bpub_date = models.DateTimeField(db_column='pub_date')
    bread = models.IntegerField(default=0)
    bcomment = models.IntegerField(null=False)
    isdelete = models.BooleanField(default=False)


class HeroInfo(models.Model):
    hname = models.CharField(max_length=10)
    hgender = models.BooleanField(default=True)
    hcontent = models.CharField(max_length=1000)
    isdelete = models.BooleanField(default=False)
    book = models.ForeignKey(BookInfo)

class AreaInfo(models.Model):
    atitle=models.CharField(max_length=20)
    aparent=models.ForeignKey('self',null=True,blank=True)