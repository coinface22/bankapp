# Generated by Django 3.2 on 2023-02-08 19:45

import core.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0006_rename_next_of_name_account_next_of_kin_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='OtherAccount',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('account_number', models.CharField(max_length=10, unique=True, validators=[core.models.numeric_validation])),
                ('balance', models.BigIntegerField()),
                ('bank', models.CharField(max_length=100)),
                ('account_type', models.CharField(choices=[('current', 'current'), ('savings', 'savings')], default='savings', max_length=10)),
                ('first_name', models.CharField(max_length=256)),
                ('middle_name', models.CharField(blank=True, max_length=256)),
                ('last_name', models.CharField(max_length=256)),
            ],
        ),
    ]