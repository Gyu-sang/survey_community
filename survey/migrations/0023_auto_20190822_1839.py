# Generated by Django 2.1.7 on 2019-08-22 18:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('survey', '0022_post_notice'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='link',
            field=models.URLField(),
        ),
    ]
