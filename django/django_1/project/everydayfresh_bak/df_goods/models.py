from django.db import models
from tinymce.models import HTMLField

# Create your models here.
class TypeInfo(models.Model):
    ttitle = models.CharField(max_length=20)
    isdelete = models.BooleanField(default=False)
    def __str__(self):
        return self.ttitle.encode('utf-8')

class GoodsInfo(models.Model):
    gtitle = models.CharField(max_length=20)
    gpic = models.ImageField(upload_to='df_goods')
    gprice = models.DecimalField(max_digits=5,decimal_places=2)
    isdelete = models.BooleanField(default=False)
    gunit = models.CharField(max_length=20)
    gclick = models.IntegerField(default=0)
    gbrief = models.CharField(max_length=500)
    grest = models.IntegerField()
    gdetail = HTMLField()
    # gadv = models.BooleanField(default=False)
    gtype = models.ForeignKey(TypeInfo)
    def __str__(self):
        return self.gtitle.encode('utf-8')