# Generated by Django 3.0.1 on 2020-02-20 06:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('testapp', '0028_auto_20200220_1519'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='is_check',
            field=models.BooleanField(default=False, verbose_name='검사'),
        ),
    ]