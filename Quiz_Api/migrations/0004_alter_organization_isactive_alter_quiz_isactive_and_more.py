# Generated by Django 5.0.2 on 2024-02-27 08:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Quiz_Api', '0003_remove_quizanswers_status_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='organization',
            name='isActive',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='quiz',
            name='isActive',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='quizanswers',
            name='isActive',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='quizquestions',
            name='isActive',
            field=models.BooleanField(default=True),
        ),
    ]
