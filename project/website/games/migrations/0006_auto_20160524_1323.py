# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-05-24 13:23
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('games', '0005_auto_20160524_1317'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='game',
            options={'ordering': ['-game_date']},
        ),
    ]
