# Generated by Django 3.2.12 on 2022-12-04 00:46

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('applications', '0023_taskstatus'),
    ]

    operations = [
        migrations.CreateModel(
            name='PageRequest',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('status', models.CharField(choices=[('P', 'Pending'), ('G', 'Generating'), ('R', 'Ready'), ('E', 'Error')], default='P', max_length=2)),
                ('error_msg', models.CharField(blank=True, max_length=128, null=True)),
                ('pdf_file', models.FileField(blank=True, null=True, upload_to='pdfs')),
                ('template_src', models.CharField(max_length=200)),
                ('base_url', models.CharField(max_length=200)),
                ('context', models.CharField(max_length=200)),
                ('season', models.CharField(max_length=200)),
            ],
        ),
        migrations.DeleteModel(
            name='TaskStatus',
        ),
    ]
