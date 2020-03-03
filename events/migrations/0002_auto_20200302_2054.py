# Generated by Django 3.0.3 on 2020-03-03 00:54

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('eventtypes', '0002_auto_20200302_2054'),
        ('repeattypes', '0002_auto_20200302_2054'),
        ('events', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='description',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='event',
            name='end_date',
            field=models.DateTimeField(null=True),
        ),
        migrations.AlterField(
            model_name='event',
            name='event_type_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='eventtypes.EventType'),
        ),
        migrations.AlterField(
            model_name='event',
            name='is_hidden',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='event',
            name='repeat_type_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='repeattypes.RepeatType'),
        ),
        migrations.AlterField(
            model_name='event',
            name='start_date',
            field=models.DateTimeField(blank=True, default=datetime.datetime.now),
        ),
    ]
