# Generated by Django 3.2.2 on 2021-06-07 23:01

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('core', '0008_auto_20210520_1234'),
    ]

    operations = [
        migrations.AlterField(
            model_name='team',
            name='users',
            field=models.ManyToManyField(related_name='user_team', to=settings.AUTH_USER_MODEL),
        ),
    ]
