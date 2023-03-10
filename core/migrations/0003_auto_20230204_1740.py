# Generated by Django 3.2 on 2023-02-04 16:40

import core.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_auto_20230203_1700'),
    ]

    operations = [
        migrations.AddField(
            model_name='account',
            name='address',
            field=models.CharField(blank=True, max_length=40),
        ),
        migrations.AddField(
            model_name='account',
            name='city',
            field=models.CharField(blank=True, max_length=20),
        ),
        migrations.AddField(
            model_name='account',
            name='contact',
            field=models.CharField(blank=True, max_length=12, validators=[core.models.numeric_validation]),
        ),
        migrations.AlterField(
            model_name='account',
            name='account_number',
            field=models.CharField(max_length=10, unique=True, validators=[core.models.numeric_validation]),
        ),
    ]
