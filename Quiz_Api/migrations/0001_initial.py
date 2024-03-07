# Generated by Django 5.0.2 on 2024-03-07 09:14

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Organization',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('isActive', models.BooleanField(default=True)),
                ('groupId', models.CharField(default=1, max_length=40)),
                ('createdDate', models.DateTimeField(auto_now_add=True)),
                ('updatedDate', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=255)),
                ('isVerified', models.BooleanField(default=False)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Quiz',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('isActive', models.BooleanField(default=True)),
                ('groupId', models.CharField(default=1, max_length=40)),
                ('createdDate', models.DateTimeField(auto_now_add=True)),
                ('updatedDate', models.DateTimeField(auto_now=True)),
                ('title', models.CharField(max_length=250)),
                ('startDate', models.DateField()),
                ('endDate', models.DateField()),
                ('resultDate', models.DateField()),
                ('prize', models.CharField(max_length=150)),
                ('duration', models.CharField(max_length=50)),
                ('totalQuestions', models.IntegerField(default=None, null=True)),
                ('order', models.IntegerField()),
                ('isVerified', models.BooleanField(default=False)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='QuizOptions',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('isActive', models.BooleanField(default=True)),
                ('groupId', models.CharField(default=1, max_length=40)),
                ('createdDate', models.DateTimeField(auto_now_add=True)),
                ('updatedDate', models.DateTimeField(auto_now=True)),
                ('option', models.TextField()),
                ('correctOption', models.BooleanField(default=False)),
                ('order', models.IntegerField(blank=True, null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='QuizQuestions',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('isActive', models.BooleanField(default=True)),
                ('groupId', models.CharField(default=1, max_length=40)),
                ('createdDate', models.DateTimeField(auto_now_add=True)),
                ('updatedDate', models.DateTimeField(auto_now=True)),
                ('question', models.TextField()),
                ('type', models.CharField(choices=[('radio', 'Radio'), ('checkbox', 'Checkbox')], max_length=150)),
                ('level', models.CharField(max_length=100)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
