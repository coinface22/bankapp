# Generated by Django 3.2 on 2023-02-08 15:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_auto_20230208_1502'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='means_of_id',
            field=models.CharField(blank=True, choices=[('nid', 'national id card'), ('dl', 'driver licence'), ('vc', 'Voters Card'), ('ip', 'International Passport')], max_length=10),
        ),
    ]
