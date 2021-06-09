# Generated by Django 3.2.2 on 2021-05-19 19:31

import core.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_auto_20210517_1436'),
    ]

    operations = [
        migrations.AddField(
            model_name='homework',
            name='pic',
            field=models.ImageField(default='users/default_pic.jpg', upload_to=core.models.homeworks_pic_path),
        ),
        migrations.AddField(
            model_name='lesson',
            name='pic',
            field=models.ImageField(default='users/default_pic.jpg', upload_to=core.models.lessons_pic_path),
        ),
        migrations.AddField(
            model_name='lessonsblock',
            name='pic',
            field=models.ImageField(default='users/default_pic.jpg', upload_to=core.models.lessonsblocks_pic_path),
        ),
    ]
