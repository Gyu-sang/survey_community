# Generated by Django 2.1.7 on 2019-08-15 08:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_auto_20190815_1657'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='answer',
            field=models.IntegerField(blank=True, default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='profile',
            name='question',
            field=models.IntegerField(blank=True, default=0),
            preserve_default=False,
        ),
    ]
