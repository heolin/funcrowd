# Generated by Django 2.0.8 on 2019-02-28 00:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('statistics', '0009_auto_20190228_0009'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='missionstats',
            name='agreement_mean',
        ),
    ]