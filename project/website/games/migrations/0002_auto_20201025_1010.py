# Generated by Django 3.1.2 on 2020-10-25 10:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('games', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='game',
            name='game_place',
        ),
        migrations.AddField(
            model_name='game',
            name='status',
            field=models.PositiveSmallIntegerField(choices=[[0, 'Started'], [1, 'Finished']], default=1),
            preserve_default=False,
        ),
    ]
