# Generated by Django 2.0.8 on 2019-03-22 10:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0016_itemtemplatefield_comment'),
    ]

    operations = [
        migrations.AlterField(
            model_name='itemtemplate',
            name='name',
            field=models.CharField(max_length=100),
        ),
    ]