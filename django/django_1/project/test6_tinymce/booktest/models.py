from django.db import models
from tinymce.models import HTMLField

# Create your models here.
class Test1(models.Model):
    content = HTMLField()
