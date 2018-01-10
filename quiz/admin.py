from django.contrib import admin

from .forms import QuestionForm
from .models import *


class TopicAdmin (admin.ModelAdmin):
    search_fields = ('topic',)


class QuestionAdmin(admin.StackedInline):
    form = QuestionForm
    model = Question
    ordering = ("order_in_quiz",)
    extra = 1


class QuizAdmin(admin.ModelAdmin):
    inlines = [QuestionAdmin]


admin.site.register(Quiz, QuizAdmin)
#admin.site.register(Question, QuestionAdmin)
#admin.site.register(Topic, TopicAdmin)
