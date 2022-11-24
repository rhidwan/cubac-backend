# Generated by Django 3.2.12 on 2022-11-24 05:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0012_auto_20221122_1223'),
    ]

    operations = [
        migrations.AlterField(
            model_name='educationalbackground',
            name='area_major',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='educationalbackground',
            name='degree',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='educationalbackground',
            name='division_class_cgpa',
            field=models.CharField(blank=True, max_length=30, null=True),
        ),
        migrations.AlterField(
            model_name='educationalbackground',
            name='institute',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='educationalbackground',
            name='passing_year',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
    ]