# Generated by Django 5.0.2 on 2024-04-10 12:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Quiz_Api', '0013_quizenrollment_quiz_api_qu_quiz_id_882332_idx'),
    ]

    operations = [
        migrations.RemoveIndex(
            model_name='quiz',
            name='Quiz_Api_qu_startDa_7670ac_idx',
        ),
        migrations.RemoveIndex(
            model_name='quizenrollment',
            name='Quiz_Api_qu_quiz_id_882332_idx',
        ),
    ]
