# Generated by Django 3.2.2 on 2021-06-08 01:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0010_lessonblockrating'),
    ]

    operations = [
        migrations.AddField(
            model_name='donehomework',
            name='comment',
            field=models.TextField(default=' '),
            preserve_default=False,
        ),
    ]
