# Generated by Django 2.0b1 on 2017-12-06 17:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0010_quiz_topic'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='questionattempt',
            name='attempt',
        ),
        migrations.RemoveField(
            model_name='questionattempt',
            name='question',
        ),
        migrations.RemoveField(
            model_name='questionattempt',
            name='response',
        ),
        migrations.RemoveField(
            model_name='quizattempt',
            name='quiz',
        ),
        migrations.RemoveField(
            model_name='quizattempt',
            name='student',
        ),
        migrations.RemoveField(
            model_name='answer',
            name='is_correct',
        ),
        migrations.DeleteModel(
            name='QuestionAttempt',
        ),
        migrations.DeleteModel(
            name='QuizAttempt',
        ),
    ]
