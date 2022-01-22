# Generated by Django 3.2.9 on 2022-01-07 22:42

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('staff_stuff', '0008_staff_card_pic'),
    ]

    operations = [
        migrations.AddField(
            model_name='staff',
            name='uname',
            field=models.SlugField(default='ok', max_length=128, unique=True, validators=[django.core.validators.RegexValidator('^[a-zA-Z0-9_]*$')]),
            preserve_default=False,
        ),
    ]