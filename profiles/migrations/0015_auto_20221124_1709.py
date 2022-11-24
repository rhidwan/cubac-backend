# Generated by Django 3.2.12 on 2022-11-24 17:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0014_auto_20221124_1702'),
    ]

    operations = [
        migrations.AlterField(
            model_name='achievementmembership',
            name='year',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='basicinfo',
            name='nationality',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='basicinfo',
            name='phone_number',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='basicinfo',
            name='work_phone',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='educationalbackground',
            name='passing_year',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]
