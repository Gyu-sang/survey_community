# Generated by Django 2.1.7 on 2019-08-16 07:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('survey', '0008_post_real_participant'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='real_participant',
        ),
    ]
