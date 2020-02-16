# Generated by Django 2.2.4 on 2020-02-09 19:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('feedback', '0013_auto_20191112_0757'),
    ]

    operations = [
        migrations.AlterField(
            model_name='feedback',
            name='type',
            field=models.CharField(choices=[('NONE', 'None'), ('CONFIRM_ONLY', 'Confirm only'), ('BINARY', 'Binary'), ('QUIZ', 'Quiz'), ('QUESTIONNAIRE', 'Questionnaire'), ('POINTS', 'Points'), ('NER', 'NER'), ('CLASSIFICATION', 'Classification')], default='NONE', max_length=32),
        ),
    ]