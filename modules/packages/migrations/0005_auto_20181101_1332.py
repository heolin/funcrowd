# Generated by Django 2.0.8 on 2018-11-01 13:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('packages', '0004_auto_20181030_2128'),
    ]

    operations = [
        migrations.AlterField(
            model_name='missionpackages',
            name='mission',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='packages', to='tasks.Mission'),
        ),
    ]
