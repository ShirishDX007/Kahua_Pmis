# Generated by Django 4.2.9 on 2024-08-22 18:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pmis', '0007_task_end_date_task_start_date_alter_client_user_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='task',
            old_name='end_date',
            new_name='task_end_date',
        ),
        migrations.RenameField(
            model_name='task',
            old_name='start_date',
            new_name='task_start_date',
        ),
    ]
