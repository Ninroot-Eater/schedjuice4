# Generated by Django 4.0.1 on 2022-01-20 10:44

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('staff_stuff', '0011_auto_20220109_1824'),
    ]

    operations = [
        migrations.AddField(
            model_name='staff',
            name='ms_id',
            field=models.CharField(default=datetime.datetime(2022, 1, 20, 10, 44, 52, 956082, tzinfo=utc), max_length=256, unique=True),
            preserve_default=False,
        ),
    ]
