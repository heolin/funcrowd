# Generated by Django 2.0.8 on 2018-11-26 22:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0003_auto_20181123_1511'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='annotation',
            name='is_done',
        ),
    ]
