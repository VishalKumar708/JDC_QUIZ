# Generated by Django 5.0.2 on 2024-04-10 11:03

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Quiz_Api', '0011_remove_quizenrollment_score'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddIndex(
            model_name='quiz',
            index=models.Index(fields=['startDate', 'endDate', 'resultDate'], name='Quiz_Api_qu_startDa_7670ac_idx'),

        ),
    ]
