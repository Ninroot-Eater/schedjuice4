# Generated by Django 4.0.2 on 2022-05-25 13:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('student_stuff', '0008_alter_student_ph_num'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='student_id',
            field=models.CharField(max_length=256, null=True, unique=True),
        ),
    ]
