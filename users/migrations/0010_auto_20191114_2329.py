# Generated by Django 2.2.7 on 2019-11-14 23:29

from django.db import migrations, models
import users.models.manager


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0009_auto_20191112_2237'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='endworker',
            managers=[
                ('objects', users.models.manager.EndWorkerManager()),
            ],
        ),
        migrations.AlterField(
            model_name='activationtoken',
            name='token',
            field=models.CharField(default='6b97d225d8e64b338439704234628263', max_length=32),
        ),
        migrations.AlterField(
            model_name='endworker',
            name='email',
            field=models.EmailField(max_length=254, unique=True, verbose_name='email address'),
        ),
        migrations.AlterField(
            model_name='passwordtoken',
            name='token',
            field=models.CharField(default='96df696d9a0d426e997baf4b5fcb8312', max_length=32),
        ),
    ]
