# Generated by Django 5.0.3 on 2024-05-03 06:07

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_alter_task_due_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='due_date',
            field=models.DateTimeField(default=datetime.datetime(2024, 5, 10, 6, 7, 3, 100089, tzinfo=datetime.timezone.utc)),
        ),
    ]
