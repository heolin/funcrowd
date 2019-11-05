# Generated by Django 2.0.8 on 2019-11-05 23:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('feedback', '0009_feedback_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='feedback',
            name='type',
            field=models.CharField(choices=[('NONE', 'None'), ('BINARY', 'Binary'), ('QUIZ', 'Quiz'), ('QUESTIONNAIRE', 'Questionnaire'), ('POINTS', 'Points'), ('NER', 'NER'), ('CLASSIFICATION', 'Classification')], default='NONE', max_length=32),
        ),
    ]
