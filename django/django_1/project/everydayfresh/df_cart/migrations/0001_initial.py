# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('df_user', '0002_auto_20180308_1725'),
        ('df_goods', '0002_auto_20180311_2026'),
    ]

    operations = [
        migrations.CreateModel(
            name='Cart',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('cgoods_count', models.IntegerField()),
                ('cgoods', models.ForeignKey(to='df_goods.GoodsInfo')),
                ('cuser', models.ForeignKey(to='df_user.UserInfo')),
            ],
        ),
    ]
