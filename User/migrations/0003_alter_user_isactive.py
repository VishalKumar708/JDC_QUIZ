# Generated by Django 5.0.2 on 2024-02-27 08:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('User', '0002_alter_user_createdby_alter_user_updatedby'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='isActive',
            field=models.BooleanField(default=True),
        ),
    ]
