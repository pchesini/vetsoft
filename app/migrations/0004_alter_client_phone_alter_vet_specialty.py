# Generated by Django 5.0.4 on 2024-06-04 21:37

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_merge_0002_provider_address_0002_vet_specialty'),
    ]

    operations = [
        migrations.AlterField(
            model_name='client',
            name='phone',
            field=models.BigIntegerField(validators=[django.core.validators.RegexValidator(message='El teléfono debe contener solo números y ser mayor a cero.', regex='^\\d+$')]),
        ),
        migrations.AlterField(
            model_name='vet',
            name='specialty',
            field=models.CharField(choices=[('Sin especialidad', 'Sin especialidad'), ('Cardiología', 'Cardiología'), ('Medicina interna de pequeños animales', 'Medicina interna de pequeños animales'), ('Medicina interna de grandes animales', 'Medicina interna de grandes animales'), ('Neurología', 'Neurología'), ('Oncología', 'Oncología'), ('Nutrición', 'Nutrición')], default='Sin especialidad', max_length=100),
        ),
    ]
