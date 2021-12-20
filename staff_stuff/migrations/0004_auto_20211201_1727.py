# Generated by Django 3.2.9 on 2021-12-01 09:27

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('staff_stuff', '0003_auto_20211130_1332'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='stafftag',
            options={'ordering': ['-id'], 'verbose_name': 'stafftag relation', 'verbose_name_plural': 'stafftag relations'},
        ),
        migrations.RemoveField(
            model_name='staff',
            name='department',
        ),
        migrations.AddField(
            model_name='stafftag',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='stafftag',
            name='pos',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='stafftag',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name='tag',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='tag',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.CreateModel(
            name='StaffDepartment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pos', models.IntegerField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('department', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='staff_stuff.department')),
                ('staff', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'staffdepartment relation',
                'verbose_name_plural': 'staffdepartment relations',
                'ordering': ['-id'],
            },
        ),
    ]