# Generated by Django 3.2.9 on 2022-01-09 10:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('role_stuff', '0002_alter_role_description'),
        ('work_stuff', '0006_auto_20211231_2329'),
    ]

    operations = [
        migrations.AddField(
            model_name='staffsession',
            name='role',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='role_stuff.role'),
        ),
        migrations.AddField(
            model_name='staffwork',
            name='role',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='role_stuff.role'),
        ),
    ]
