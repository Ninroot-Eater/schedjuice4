# Generated by Django 3.2.9 on 2021-12-06 05:02

import datetime
import django.core.validators
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('work_stuff', '0002_session_staffsession'),
    ]

    operations = [
        migrations.AddField(
            model_name='session',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=datetime.datetime(2021, 12, 6, 5, 2, 6, 86446, tzinfo=utc)),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='session',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name='staffsession',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=datetime.datetime(2021, 12, 6, 5, 2, 9, 560781, tzinfo=utc)),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='staffsession',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name='staffwork',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=datetime.datetime(2021, 12, 6, 5, 2, 14, 53413, tzinfo=utc)),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='staffwork',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='work',
            name='meeting_id',
            field=models.CharField(default='not provided', max_length=20, validators=[django.core.validators.RegexValidator('^\\d{1,11}$ ')]),
        ),
    ]