

# Create your models here.

from django.db import models
from django.utils.encoding import python_2_unicode_compatible

# a lazy version of a unicode version of a translatable string
# good practice for models.
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User


BOOL_CHOICES = (
    (True, 'Yes'),
    (False, 'No')
)


"""""
class Topic(models.Model):
    topic = models.CharField(verbose_name=_('Topic'), max_length=250, blank=True, unique=True, null=True)
    
    class Meta:
        verbose_name =_('Topic')
        verbose_name_plural = _('Topics')
    
    def __str__(self):
        return self.topic
"""""

class Quiz(models.Model):
    #Represents a quiz
    date_created = models.DateTimeField(
        auto_now_add=True
    )

    #topic = models.ForeignKey(Topic, null=True, blank=True, on_delete=models.CASCADE)

    date_modified = models.DateTimeField(
        auto_now=True
    )
    title = models.CharField(
        _('Quizc Title'),
        max_length=140,
        help_text=_(
            'The title of this quiz.'
        )
    )
    content = models.TextField(
        _('Quiz Content'),
        help_text=_(
            'The instructional content of this quiz.'
        )
    )

    class Meta:
        verbose_name = _('Quiz')
        verbose_name_plural = _('Quizzes')
        ordering = ('-date_created', '-date_modified',)

    def __str__(self):
        return self.title

    def possible(self):
        total = 0
        for question in self.questions.all():
            question.save()
            total += question.value
        return total



class Question(models.Model):

    # Represents a question pertaining to a Lesson.

    quiz = models.ForeignKey(Quiz,related_name='questions', on_delete=models.CASCADE)
    order_in_quiz = models.PositiveIntegerField(_('Order in Quiz'))

    question = models.CharField(
        _('Question'),
        max_length=1000,blank=False,
        help_text=_(
            "A question that can be answered with either 'Yes' or 'No'."
        )
    )
    correct_answer = models.BooleanField(
        _('Correct Answer'),
        choices=BOOL_CHOICES,
        default=True
    )

    class Meta:
        verbose_name = _('Question')
        verbose_name_plural = _('Questions')
        ordering = ('order_in_quiz',)

    def __str__(self):
        return self.question



class Answer(models.Model):

    #Represents an answer by a user to a Question

    question = models.ForeignKey(
        Question,
        editable=False,  on_delete=models.CASCADE)

    #content = models.CharField(max_length=1000, blank=False, help_text='')
    user = models.ForeignKey(
        'auth.User',
        editable=False,
        related_name='quiz_answers', on_delete=models.CASCADE)

    answered_correctly = models.BooleanField(editable=False)



    class Meta:
        verbose_name = _('Answer')
        verbose_name_plural = _('Answers')
        unique_together = ('question', 'user')

    def __str__(self):
        return '{} - {} - {}'.format(
            self.question_id,
            self.user_id,
            self.answered_correctly
        )


