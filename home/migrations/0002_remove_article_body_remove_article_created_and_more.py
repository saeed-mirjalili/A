# Generated by Django 5.1.1 on 2024-09-16 07:21

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='article',
            name='body',
        ),
        migrations.RemoveField(
            model_name='article',
            name='created',
        ),
        migrations.AddField(
            model_name='article',
            name='pdf',
            field=models.FileField(default=django.utils.timezone.now, upload_to='%Y/%m/%d/'),
            preserve_default=False,
        ),
    ]
