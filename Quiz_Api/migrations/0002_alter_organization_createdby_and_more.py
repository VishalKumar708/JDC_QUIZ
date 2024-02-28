# Generated by Django 5.0.2 on 2024-02-27 05:52

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Quiz_Api', '0001_initial'),
        ('User', '0002_alter_user_createdby_alter_user_updatedby'),
    ]

    operations = [
        migrations.AlterField(
            model_name='organization',
            name='createdBy',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='%(class)s_createdBy', to='User.user'),
        ),
        migrations.AlterField(
            model_name='organization',
            name='updatedBy',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='%(class)s_updatedBy', to='User.user'),
        ),
        migrations.AlterField(
            model_name='quiz',
            name='createdBy',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='%(class)s_createdBy', to='User.user'),
        ),
        migrations.AlterField(
            model_name='quiz',
            name='organization',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='organization_quiz', to='Quiz_Api.organization'),
        ),
        migrations.AlterField(
            model_name='quiz',
            name='updatedBy',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='%(class)s_updatedBy', to='User.user'),
        ),
        migrations.AlterField(
            model_name='quizanswers',
            name='createdBy',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='%(class)s_createdBy', to='User.user'),
        ),
        migrations.AlterField(
            model_name='quizanswers',
            name='isVerified',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='quizanswers',
            name='updatedBy',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='%(class)s_updatedBy', to='User.user'),
        ),
        migrations.AlterField(
            model_name='quizquestions',
            name='createdBy',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='%(class)s_createdBy', to='User.user'),
        ),
        migrations.AlterField(
            model_name='quizquestions',
            name='isVerified',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='quizquestions',
            name='updatedBy',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='%(class)s_updatedBy', to='User.user'),
        ),
    ]