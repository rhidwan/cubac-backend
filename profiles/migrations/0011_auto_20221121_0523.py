# Generated by Django 3.2.12 on 2022-11-21 05:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0010_auto_20221121_0110'),
    ]

    operations = [
        migrations.AlterField(
            model_name='workexperience',
            name='organization',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='workexperience',
            name='post',
            field=models.CharField(max_length=300),
        ),
    ]
