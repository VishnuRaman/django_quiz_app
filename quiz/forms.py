from django import forms
from django.forms.fields import ChoiceField

from .models import BOOL_CHOICES, Quiz, Question


class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        widgets = {'correct_answer': forms.RadioSelect}
        fields = (
            'order_in_quiz',
            'quiz',
            'question',
            'correct_answer'
        )


class QuestionField(ChoiceField):
    default_error_messages = {'required': 'You are required to answer this question.',}
    widget = forms.widgets.RadioSelect


class AnswerQuizForm(forms.ModelForm):

    #A form for processing answers associated to a quiz.

    class Meta:
        model = Quiz
        exclude = ['title', 'content']

    def __init__(self, *args, **kwargs):
        super(AnswerQuizForm, self).__init__(*args, **kwargs)
        question_list = Question.objects.filter(quiz=self.instance).order_by('order_in_quiz')
        for i, question in enumerate(question_list, start=1):
            self.fields[ 'question__{}'.format(question.pk)] = QuestionField(label="{num}. {question}".format(
                    num=i,question=question.question),required=True,choices=BOOL_CHOICES)