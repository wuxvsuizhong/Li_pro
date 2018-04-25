from django.db import models
from df_user.models import UserInfo
from df_goods.models import GoodsInfo

# Create your models here.
class Cart(models.Model):
    cuser = models.ForeignKey(UserInfo)
    cgoods = models.ForeignKey(GoodsInfo)
    cgoods_count = models.IntegerField()