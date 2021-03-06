# Generated by Django 4.0.1 on 2022-01-21 14:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('staff_stuff', '0012_staff_ms_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='staff',
            name='city',
            field=models.CharField(default='', max_length=128),
        ),
        migrations.AddField(
            model_name='staff',
            name='country',
            field=models.CharField(default='mm', max_length=16),
        ),
        migrations.AddField(
            model_name='staff',
            name='house_num',
            field=models.CharField(default='', max_length=16),
        ),
        migrations.AddField(
            model_name='staff',
            name='postal_code',
            field=models.CharField(default='', max_length=12),
        ),
        migrations.AddField(
            model_name='staff',
            name='street',
            field=models.CharField(default='', max_length=128),
        ),
        migrations.AddField(
            model_name='staff',
            name='township',
            field=models.CharField(default='', max_length=128),
        ),
    ]
