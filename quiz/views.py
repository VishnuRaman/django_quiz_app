from django.shortcuts import render

#converts string representation of truth to true (1) or false(0)
from distutils.util import strtobool
from django.views.generic.edit import CreateView
from django.contrib.auth.models import User
from django.urls import reverse
from django.db.models import Case, IntegerField, Sum, When
from django.http import HttpResponseForbidden, HttpResponseRedirect
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.contrib.auth import authenticate, login
from .forms import TakeQuizForm
from .models import *

from django.shortcuts import  get_object_or_404
from django.views.generic import  ListView, DetailView
from django.views.generic.detail import  SingleObjectTemplateResponseMixin
from django.views.generic.edit import ProcessFormView, ModelFormMixin



"""""
def user_login(request):
    name =request.POST['username']
    password = request.POST['password']
    user = authenticate(request, username=name, password=password)
    if user is not None:
        login(request,user)
        reverse_lazy('lesson-list')
    else:
        return HttpResponse('try again')
"""



class UserRegistrationView(CreateView):
    template_name = 'registration/register.html'
    form_class = UserCreationForm
    success_url = reverse_lazy("lesson-list")

    def form_valid(self,form):
        result = super(UserRegistrationView,self).form_valid(form)
        cd = form.cleaned_data
        user= authenticate(username=cd['username'], password=cd['password1'])
        login(self.request,user)
        return result



# Mixins are a sort of class that is user to 'mix-in' extra properties and methods into a class.
class RequiredGroupMixin(object):

    # Ensure only logged in users who belong to a particular group (or groups)
    # can access this view.

    def dispatch(self, request, *args, **kwargs):
        # assert isinstance(self, ((TakeQuizView, QuizResultsListView), RequiredGroupMixin))

        # takes argument object and string, returns true if string is the name of one of the object's attribute,
        # False if not
        if hasattr(self, 'restrict_to_groups'):
            allowed_groups = request.user.groups.filter(
                name__in=self.restrict_to_groups
            )
            if not allowed_groups and request.user.is_superuser is False:
                return HttpResponseForbidden(
                    'Only users that belong to the following groups may '
                    'access this page: {}'.format(
                        ', '.join(self.restrict_to_groups)
                    ))
        data = super(RequiredGroupMixin,self).dispatch(request, *args, **kwargs)
        return data


class IsStudentOrIsAdminMixin(object):

    # Determines whether the logged-in user is an admin or a student.

    def dispatch(self, request, *args, **kwargs):
        # assert isinstance(self, ((QuizListView,QuizDetailView ), IsStudentOrIsInstructorMixin))
        is_student = False
        is_admin = False

        if request.user.groups.filter(name__in=['Students']):
            is_student = True
        if request.user.groups.filter(
            name__in=['Admins']
        ) or request.user.is_superuser:
            is_admin = True

        self.is_student = is_student
        self.is_admin = is_admin
        return super(IsStudentOrIsAdminMixin, self).dispatch(
            request, *args, **kwargs
        )

    def get_context_data(self, **kwargs):

        # Add `is_student` and `is_admin` to the template context.

        context = super(IsStudentOrIsAdminMixin, self).get_context_data(
            **kwargs)

        context['is_student'] = self.is_student
        context['is_admin'] = self.is_admin
        return context


class QuizListView(IsStudentOrIsAdminMixin,ListView):
    queryset = Quiz.objects.order_by('-date_created')
    template_name = 'quiz/quiz_list.html'
    #def get_queryset(self):
     #   return super(QuizListView,self).get_queryset()


class QuizDetailView(IsStudentOrIsAdminMixin,DetailView):
    queryset = Quiz.objects.prefetch_related('questions')
    template_name = 'quiz/quiz_detail.html'
    #print(queryset)
    #def get_queryset(self):
     #   return super(QuizDetailView,self).get_queryset()


class TakeQuizView(RequiredGroupMixin,
                   SingleObjectTemplateResponseMixin,
                   ModelFormMixin,
                   ProcessFormView):
    model = Quiz
    form_class = TakeQuizForm
    template_name = 'quiz/take_quiz.html'
    restrict_to_groups = ('Students',)

    def get_queryset(self):
        return super(TakeQuizView,self).get_queryset()

    def dispatch(self, request, *args, **kwargs):

        # Ensure self.object is set so TakeQuizForm instantiates correctly.


        self.object = self.get_object()
        return super(TakeQuizView, self).dispatch(
            request, *args, **kwargs
        )

    def convert_form_value_to_bool(self, value):

        # Converts a yes/no answer into a boolean

        return bool(strtobool(value))

    def form_valid(self, form):

        # If the form is valid, record the test-taker's answers then redirect
        # back to the 'Quiz List' page.

        for question_key, answer in form.cleaned_data.items():
            question_pk = int(question_key.split('__')[-1])
            question = self.object.questions.get(pk=question_pk)
            answer_as_bool = self.convert_form_value_to_bool(answer)
            user_answer = Answer(
                user=self.request.user,
                question=question,
                answered_correctly=answer_as_bool is question.correct_answer
            )
            user_answer.save()
        return HttpResponseRedirect(reverse('quiz-list'))


class QuizResultsListView(RequiredGroupMixin,
                          DetailView):
    queryset = Quiz.objects.prefetch_related('questions')
    template_name = 'quiz/see_quiz_results.html'
    restrict_to_groups = ('Admins',)

    def get_context_data(self, **kwargs):
        context = super(QuizResultsListView, self).get_context_data(**kwargs)
        context['total_questions'] = self.object.questions.count()
        context['student_list'] = User.objects.filter(
            groups__name__in=['Students'],
            quiz_answers__question__quiz_id=self.object.pk
        ).annotate(
            num_correct_answers=Sum(Case(When(quiz_answers__answered_correctly=True, then=1),default=0,
                                         output_field=IntegerField()))).order_by('username').distinct()
        return context

"""""""""
class TopicListView (IsStudentOrIsAdminMixin, ListView):

    queryset = Topic.objects.all()
    template_name = 'quiz/topics_list.html'


class TopicDetailView (IsStudentOrIsAdminMixin, ListView):
    #model = Quiz
    queryset = Topic.objects.prefetch_related('quizzes')
    template_name = 'quiz/topic_detail.html'

    
    def dispatch(self, request, *args, **kwargs):
        self.topic = get_object_or_404(Topic, topic=self.kwargs['pk'])
        return super(TopicDetailView,self).dispatch(request,*args,**kwargs)

    def get_context_data(self, **kwargs):
        context = super(TopicDetailView,self).get_context_data(**kwargs)
        context['topic'] = self.topic
        return context

    def get_queryset(self):
        queryset = super(TopicDetailView,self).get_queryset()
        return queryset.filter(topic=self.topic, draft=False)
    
"""""""""