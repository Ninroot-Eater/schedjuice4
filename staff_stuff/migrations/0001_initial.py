# Generated by Django 3.2.9 on 2021-11-28 04:06

import datetime
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import staff_stuff.managers


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Department',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=256)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('is_under', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='staff_stuff.department')),
            ],
        ),
        migrations.CreateModel(
            name='Staff',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('dname', models.CharField(default='Display Name', max_length=128)),
                ('ename', models.CharField(default='Nickname', max_length=128)),
                ('description', models.TextField(default='Description...')),
                ('dob', models.DateField(default=datetime.date(2000, 1, 1))),
                ('gender', models.CharField(default='', max_length=16)),
                ('ph_num', models.CharField(default='09650222', max_length=60, validators=[django.core.validators.RegexValidator('^\\d{1,11}$')])),
                ('facebook', models.CharField(default='https://facebook.com/profile', max_length=256)),
                ('region', models.CharField(default='0', max_length=8)),
                ('profile_pic', models.ImageField(default='profile_pics/default.jpg', upload_to='profile_pics')),
                ('first_day', models.DateField(default=datetime.date(2018, 1, 1))),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'staff',
                'verbose_name_plural': 'staff members',
            },
            managers=[
                ('objects', staff_stuff.managers.UserManager()),
            ],
        ),
    ]
