# Generated by Django 2.0.8 on 2018-10-22 22:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('order_strategy', '0001_initial'),
        ('tasks', '0001_initial'),
        ('packages', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='MissionPackages',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('max_annotations', models.IntegerField(default=0)),
                ('multiple_annotations', models.BooleanField(default=False)),
                ('mission', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='packages', to='tasks.Mission')),
                ('strategy', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='order_strategy.Strategy')),
            ],
        ),
        migrations.RemoveField(
            model_name='package',
            name='mission',
        ),
        migrations.AddField(
            model_name='package',
            name='parent',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='packages', to='packages.MissionPackages'),
            preserve_default=False,
        ),
    ]
