# Generated by Django 3.2.12 on 2022-07-04 05:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('call_applications', '0001_initial'),
        ('applications', '0002_application_gw_trx_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='application',
            name='call_for_application',
            field=models.ForeignKey(default='7c66dae4-1481-4d89-ac81-cedbbfbd3257', on_delete=django.db.models.deletion.CASCADE, to='call_applications.callforapplication'),
            preserve_default=False,
        ),
    ]
