# Generated by Django 3.2.12 on 2022-12-02 09:31

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('call_applications', '0006_callforapplication_skip_to'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('applications', '0019_auto_20221124_1709'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='application',
            options={'ordering': ('roll_no',)},
        ),
        migrations.AlterUniqueTogether(
            name='application',
            unique_together={('call_for_application', 'user')},
        ),
    ]
