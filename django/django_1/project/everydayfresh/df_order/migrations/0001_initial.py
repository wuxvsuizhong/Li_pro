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
            name='Order',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('order_date', models.DateTimeField(auto_now=True)),
                ('ototal', models.DecimalField(max_digits=8, decimal_places=2)),
                ('oispay', models.BooleanField(default=False)),
                ('orecaddr', models.CharField(max_length=100)),
                ('orderno', models.CharField(max_length=15)),
                ('otransfee', models.DecimalField(max_digits=6, decimal_places=2)),
                ('owner', models.ForeignKey(to='df_user.UserInfo')),
            ],
        ),
        migrations.CreateModel(
            name='OrderItem',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('goodscount', models.IntegerField()),
                ('sum', models.DecimalField(max_digits=6, decimal_places=2)),
                ('goodstype', models.ForeignKey(to='df_goods.GoodsInfo')),
                ('partof', models.ForeignKey(to='df_order.Order')),
            ],
        ),
    ]
