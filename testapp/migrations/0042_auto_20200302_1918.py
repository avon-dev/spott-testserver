# Generated by Django 3.0.1 on 2020-03-02 10:18

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('testapp', '0041_auto_20200225_1521'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='back_image',
            field=models.ImageField(blank=True, null=True, upload_to='postb'),
        ),
        migrations.AlterField(
            model_name='report',
            name='comment',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='testapp_report_comment_related', to='testapp.Comment'),
        ),
        migrations.AlterField(
            model_name='report',
            name='post',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='testapp_report_post_related', to='testapp.Post'),
        ),
        migrations.AlterField(
            model_name='report',
            name='reporter',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='testapp_report_reporter_related', to=settings.AUTH_USER_MODEL, to_field='user_uid'),
        ),
    ]
