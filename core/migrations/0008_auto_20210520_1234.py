# Generated by Django 3.2.2 on 2021-05-20 09:34

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('core', '0007_alter_donehomework_homework'),
    ]

    operations = [
        migrations.AddField(
            model_name='donehomework',
            name='done',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='donehomework',
            name='rating',
            field=models.PositiveSmallIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='donehomework',
            name='user',
            field=models.ForeignKey(default=2, on_delete=django.db.models.deletion.CASCADE, related_name='user_done_homework', to='users.user'),
            preserve_default=False,
        ),
    ]