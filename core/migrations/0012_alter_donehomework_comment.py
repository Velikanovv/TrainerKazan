# Generated by Django 3.2.2 on 2021-06-08 01:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0011_donehomework_comment'),
    ]

    operations = [
        migrations.AlterField(
            model_name='donehomework',
            name='comment',
            field=models.TextField(blank=True),
        ),
    ]
