# Generated by Django 3.0.3 on 2020-03-03 03:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('exams', '0002_auto_20200302_2118'),
    ]

    operations = [
        migrations.RenameField(
            model_name='exam',
            old_name='event_id',
            new_name='event',
        ),
    ]
