# Generated by Django 2.1.7 on 2019-08-19 07:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('survey', '0015_auto_20190819_1602'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='message',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='comment',
            name='photo',
            field=models.ImageField(upload_to=''),
        ),
    ]
