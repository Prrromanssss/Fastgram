# Generated by Django 3.2.16 on 2022-12-20 11:01

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('response', '0002_auto_20221215_1853'),
    ]

    operations = [
        migrations.AddField(
            model_name='response',
            name='likes',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL, verbose_name='лайк'),
        ),
    ]
