# Generated by Django 2.2.4 on 2020-05-13 22:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('packages', '0008_auto_20200314_1755'),
    ]

    operations = [
        migrations.AlterField(
            model_name='missionpackages',
            name='max_annotations',
            field=models.IntegerField(),
        ),
    ]