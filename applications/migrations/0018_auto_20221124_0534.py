# Generated by Django 3.2.12 on 2022-11-24 05:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('applications', '0017_seat_call_for_application'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transaction',
            name='transaction_from',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='transaction_method',
            field=models.CharField(max_length=100),
        ),
    ]
