# Generated by Django 4.2.11 on 2024-05-02 03:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend_server', '0023_alter_myuser_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='workouttype',
            name='name',
            field=models.CharField(choices=[('VR Game', 'VR Game'), ('Cycling', 'Cycling'), ('Running', 'Running'), ('Yoga', 'Yoga'), ('Pilates', 'Pilates'), ('Aerobic', 'Aerobic'), ('High Intensity', 'High Intensity')], max_length=20),
        ),
    ]
