# Generated by Django 4.0.1 on 2022-01-21 14:30

import datetime
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('work_stuff', '0008_work_ms_id'),
    ]

    operations = [
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('ms_id', models.CharField(max_length=256, unique=True)),
                ('dname', models.CharField(default='Display Name', max_length=128)),
                ('ename', models.CharField(default='Nickname', max_length=128)),
                ('description', models.TextField(default='Description...')),
                ('status', models.CharField(default='active', max_length=128)),
                ('dob', models.DateField(default=datetime.date(2000, 1, 1))),
                ('gender', models.CharField(default='', max_length=32)),
                ('ph_num', models.CharField(max_length=16, validators=[django.core.validators.RegexValidator('^\\d{1,11}$')])),
                ('profile_pic', models.ImageField(default='stu_profile/default.jpg', upload_to='stu_profile')),
                ('cover_pic', models.ImageField(default='stu_cover/default.jpg', upload_to='stu_cover')),
                ('card_pic', models.ImageField(default='stu_card/default.jpg', upload_to='stu_card')),
                ('house_num', models.CharField(default='', max_length=16)),
                ('street', models.CharField(default='', max_length=128)),
                ('township', models.CharField(default='', max_length=128)),
                ('city', models.CharField(default='', max_length=128)),
                ('region', models.CharField(default='0', max_length=4)),
                ('country', models.CharField(default='mm', max_length=16)),
                ('postal_code', models.CharField(default='', max_length=12)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'student',
                'verbose_name_plural': 'students',
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='StudentWork',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='student_stuff.student')),
                ('work', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='work_stuff.work')),
            ],
            options={
                'verbose_name': 'student_work',
                'verbose_name_plural': 'student_works',
                'ordering': ['id'],
            },
        ),
    ]