from django.db import models



# Create your models here.
class Order(models.Model):
    owner = models.ForeignKey('df_user.UserInfo')
    order_date = models.DateTimeField(auto_now=True)
    ototal = models.DecimalField(max_digits=8,decimal_places=2)
    oispay = models.BooleanField(default=False)
    orecaddr = models.CharField(max_length=100)
    orderno = models.CharField(max_length=15)
    otransfee = models.DecimalField(max_digits=6,decimal_places=2)

class OrderItem(models.Model):
    goodstype = models.ForeignKey('df_goods.GoodsInfo')
    goodscount = models.IntegerField()
    sum = models.DecimalField(max_digits=6,decimal_places=2)
    partof = models.ForeignKey(Order)