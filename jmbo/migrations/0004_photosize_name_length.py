# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-05-30 12:47
from __future__ import unicode_literals

from django.core.validators import RegexValidator
from django.db import migrations, models
from django.utils import timezone


# We're modifying a field from another app. This requires trickery.

def fix_app_label(apps, schema_editor):
    migrations.recorder.MigrationRecorder.Migration.objects.create(
        app='jmbo', name='0004_photosize_name_length',
        applied=timezone.now()
    )


class Migration(migrations.Migration):
    dependencies = [
        ('jmbo', '0003_auto_20160530_1247'),
    ]

    operations = [
        migrations.AlterField(
            model_name='photosize',
            name='name',
            field=models.CharField(unique=True, max_length=255, validators=[RegexValidator(regex='^[a-z0-9_]+$', message='Use only plain lowercase letters (ASCII), numbers and underscores.')]),
        ),
        migrations.RunPython(fix_app_label)
    ]

    def __init__(self, *args, **kwargs):
        super(Migration, self).__init__(*args, **kwargs)
        self.app_label = 'photologue'
