from django.db import models

# Create your models here.
class BookInfo(models.Model):
    class Meta():
        db_table='bookinfo'
    btitle=models.CharField(max_length=20)
    bpub_date=models.DateTimeField(db_column='pub_date')
    bread=models.IntegerField()
    bcomment=models.IntegerField()
    isdelete=models.BooleanField()

class HeroInfo(models.Model):
    hname=models.CharField(max_length=10)
    hgender=models.BooleanField()
    hcontent=models.CharField(max_length=1000)
    isdelete=models.BooleanField()
    book=models.ForeignKey('BookInfo')

    def show_name(self):
        return self.hname

