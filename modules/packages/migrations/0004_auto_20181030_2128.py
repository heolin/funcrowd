# Generated by Django 2.0.8 on 2018-10-30 21:28

from django.db import migrations
import sortedm2m.fields


class Migration(migrations.Migration):

    dependencies = [
        ('packages', '0003_auto_20181030_2004'),
    ]

    operations = [
        migrations.AlterField(
            model_name='package',
            name='items',
            field=sortedm2m.fields.SortedManyToManyField(help_text=None, to='tasks.Item'),
        ),
    ]