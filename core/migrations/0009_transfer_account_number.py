# Generated by Django 3.2 on 2023-02-11 13:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0008_otheraccount_date_created'),
    ]

    operations = [
        migrations.AddField(
            model_name='transfer',
            name='account_number',
            field=models.CharField(blank=True, max_length=12, null=True),
        ),
    ]