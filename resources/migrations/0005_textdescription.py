# Generated by Django 2.0.2 on 2018-03-25 17:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('resources', '0004_auto_20180313_2314'),
    ]

    operations = [
        migrations.CreateModel(
            name='TextDescription',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
            ],
        ),
    ]