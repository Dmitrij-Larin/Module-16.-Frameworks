# Generated by Django 5.0.13 on 2025-04-02 23:24

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dogs', '0002_dog'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dog',
            name='birth_date',
            field=models.DateField(blank=True, null=True, verbose_name='Дата рождения'),
        ),
        migrations.AlterField(
            model_name='dog',
            name='breed',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dogs.breed', verbose_name='Порода'),
        ),
        migrations.AlterField(
            model_name='dog',
            name='name',
            field=models.CharField(max_length=150, verbose_name='Кличка'),
        ),
        migrations.AlterField(
            model_name='dog',
            name='photo',
            field=models.ImageField(blank=True, null=True, upload_to='dogs/', verbose_name='Изображение'),
        ),
    ]
