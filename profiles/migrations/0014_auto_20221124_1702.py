# Generated by Django 3.2.12 on 2022-11-24 17:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0013_auto_20221124_0534'),
    ]

    operations = [
        migrations.AlterField(
            model_name='achievementmembership',
            name='organization',
            field=models.CharField(max_length=250),
        ),
        migrations.AlterField(
            model_name='educationalbackground',
            name='division_class_cgpa',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='workexperience',
            name='from_date',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='workexperience',
            name='to_date',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]