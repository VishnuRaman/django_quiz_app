# Generated by Django 2.0b1 on 2017-11-24 12:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0005_answer_is_correct'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='quiz',
            options={'ordering': ('-date_created', '-date_modified'), 'verbose_name': 'Quiz', 'verbose_name_plural': 'Quizzes'},
        ),
        migrations.RemoveField(
            model_name='question',
            name='topic',
        ),
        migrations.RemoveField(
            model_name='quiz',
            name='topic',
        ),
        migrations.DeleteModel(
            name='Topic',
        ),
    ]
