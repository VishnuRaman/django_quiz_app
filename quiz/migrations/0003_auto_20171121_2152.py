# Generated by Django 2.0b1 on 2017-11-21 21:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0002_answer_content'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='question',
            name='content',
        ),
        migrations.AlterField(
            model_name='question',
            name='question',
            field=models.CharField(help_text="A question that can be answered with either 'Yes' or 'No'.", max_length=1000, verbose_name='Question'),
        ),
    ]
