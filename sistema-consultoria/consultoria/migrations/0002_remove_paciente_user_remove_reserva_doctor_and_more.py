# Generated by Django 4.2.3 on 2023-09-21 06:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('consultoria', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='paciente',
            name='user',
        ),
        migrations.RemoveField(
            model_name='reserva',
            name='doctor',
        ),
        migrations.RemoveField(
            model_name='reserva',
            name='user',
        ),
        migrations.DeleteModel(
            name='Doctor',
        ),
        migrations.DeleteModel(
            name='Paciente',
        ),
        migrations.DeleteModel(
            name='Reserva',
        ),
    ]
