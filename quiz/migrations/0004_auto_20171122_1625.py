# Generated by Django 2.0b1 on 2017-11-22 16:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0003_auto_20171121_2152'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='answer',
            options={'verbose_name': 'Answer', 'verbose_name_plural': 'Answers'},
        ),
        migrations.RemoveField(
            model_name='answer',
            name='content',
        ),
        migrations.RemoveField(
            model_name='answer',
            name='is_correct',
        ),
    ]
