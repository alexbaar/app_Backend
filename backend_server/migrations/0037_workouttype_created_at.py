# Generated by Django 4.2.11 on 2024-05-03 06:38

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('backend_server', '0036_alter_workouttype_email'),
    ]

    operations = [
        migrations.AddField(
            model_name='workouttype',
            name='created_at',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]