# Generated by Django 3.2.3 on 2022-07-21 19:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog_app', '0005_auto_20220720_1832'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='poll',
            name='total_votes',
        ),
    ]
