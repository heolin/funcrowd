# Generated by Django 2.0.8 on 2019-10-01 07:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('achievements', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='achievement',
            name='target',
            field=models.FloatField(default=1),
        ),
    ]