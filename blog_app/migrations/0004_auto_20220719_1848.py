# Generated by Django 3.2.3 on 2022-07-19 18:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('blog_app', '0003_poll_question'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='poll',
            options={'ordering': ['total_votes']},
        ),
        migrations.AddField(
            model_name='poll',
            name='total_votes',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='poll',
            name='post',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='blog_app.post'),
        ),
    ]