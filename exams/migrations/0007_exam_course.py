# Generated by Django 3.0.3 on 2020-03-21 01:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0001_initial'),
        ('exams', '0006_remove_exam_course'),
    ]

    operations = [
        migrations.AddField(
            model_name='exam',
            name='course',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.DO_NOTHING, to='courses.Course'),
            preserve_default=False,
        ),
    ]