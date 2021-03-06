# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-09-12 02:47
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('workorder', '0008_svn_workorder_domain_time'),
    ]

    operations = [
        migrations.AddField(
            model_name='data_workorder',
            name='sql_action_status',
            field=models.CharField(blank=True, choices=[(b'add', '\u589e'), (b'del', '\u5220'), (b'change', '\u6539'), (b'find', '\u67e5'), (b'other', '\u5176\u4ed6')], default=b'other', max_length=10, null=True, verbose_name='\u64cd\u4f5c'),
        ),
        migrations.AddField(
            model_name='data_workorder',
            name='sql_name',
            field=models.CharField(default=1, max_length=100, verbose_name='\u6570\u636e\u5e93\u6216\u8868'),
            preserve_default=False,
        ),
    ]
