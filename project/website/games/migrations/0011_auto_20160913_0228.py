# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-09-13 02:28
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('games', '0010_gameround_is_damaten'),
    ]

    operations = [
        migrations.AddField(
            model_name='game',
            name='rate',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=6),
        ),
        migrations.AlterField(
            model_name='game',
            name='game_rule',
            field=models.PositiveSmallIntegerField(choices=[(0, 'Unknown'), (1, 'Tonpusen. No tanyao, no red fives'), (2, 'Tonpusen. Tanyao, no red fives'), (3, 'Tonpusen. Tanyao, red fives'), (4, 'Tonpusen. Tanyao, red fives. Fast'), (5, 'Hanchan. No tanyao, no red fives'), (6, 'Hanchan. Tanyao, no red fives'), (7, 'Hanchan. Tanyao, red fives'), (8, 'Hanchan. Tanyao, red fives. Fast')], default=0),
        ),
    ]