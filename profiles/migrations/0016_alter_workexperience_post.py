# Generated by Django 3.2.12 on 2022-11-24 17:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0015_auto_20221124_1709'),
    ]

    operations = [
        migrations.AlterField(
            model_name='workexperience',
            name='post',
            field=models.TextField(),
        ),
    ]