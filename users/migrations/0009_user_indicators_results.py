# Generated by Django 3.2.2 on 2021-05-23 14:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0008_user_c_pass'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='indicators_results',
            field=models.ManyToManyField(blank=True, related_name='user_indicators_results', to='users.IndicatorsExerciseResult'),
        ),
    ]
