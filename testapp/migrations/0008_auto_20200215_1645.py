# Generated by Django 3.0.1 on 2020-02-15 07:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('testapp', '0007_auto_20200215_1641'),
    ]

    operations = [
        migrations.AlterField(
            model_name='hashtag',
            name='tag_name',
            field=models.CharField(max_length=250, unique=True, verbose_name='태그명'),
        ),
    ]