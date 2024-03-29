# Generated by Django 3.2.3 on 2022-07-21 20:31

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('blog_app', '0007_auto_20220721_2026'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='poll',
            name='option1_voters',
        ),
        migrations.RemoveField(
            model_name='poll',
            name='option2_voters',
        ),
        migrations.RemoveField(
            model_name='poll',
            name='option3_voters',
        ),
        migrations.RemoveField(
            model_name='poll',
            name='option4_voters',
        ),
        migrations.AddField(
            model_name='poll',
            name='option1_value',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='poll',
            name='option2_value',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='poll',
            name='option3_value',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='poll',
            name='option4_value',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='poll',
            name='total_voters',
            field=models.ManyToManyField(blank=True, related_name='blogpost_poll', to=settings.AUTH_USER_MODEL),
        ),
    ]
