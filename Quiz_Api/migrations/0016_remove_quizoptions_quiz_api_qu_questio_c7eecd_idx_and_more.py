# Generated by Django 5.0.2 on 2024-04-12 09:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Quiz_Api', '0015_quizoptions_quiz_api_qu_questio_c7eecd_idx_and_more'),
    ]

    operations = [
        migrations.RemoveIndex(
            model_name='quizoptions',
            name='Quiz_Api_qu_questio_c7eecd_idx',
        ),
        migrations.RemoveIndex(
            model_name='quizquestions',
            name='Quiz_Api_qu_quiz_id_c9ab72_idx',
        ),
    ]