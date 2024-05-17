# Generated by Django 4.2.11 on 2024-05-02 11:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('backend_server', '0024_alter_workouttype_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='workouttype',
            name='session_id',
            field=models.UUIDField(null=True, unique=True),
        ),
        migrations.AlterField(
            model_name='helpcentremessage',
            name='thread_number',
            field=models.UUIDField(default='', unique=True),
        ),
        migrations.AlterField(
            model_name='workoutentry',
            name='session_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='workout_sessions', to='backend_server.workouttype', to_field='session_id'),
        ),
    ]
