# Generated by Django 3.2.2 on 2021-05-17 08:37

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('core', '0002_auto_20210517_1135'),
    ]

    operations = [
        migrations.AlterField(
            model_name='homework',
            name='done',
            field=models.ManyToManyField(blank=True, related_name='homework_done', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='homework',
            name='not_done',
            field=models.ManyToManyField(blank=True, related_name='homework_not_done', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='lesson',
            name='done',
            field=models.ManyToManyField(blank=True, related_name='lesson_done', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='lesson',
            name='not_done',
            field=models.ManyToManyField(blank=True, related_name='lesson_not_done', to=settings.AUTH_USER_MODEL),
        ),
    ]
