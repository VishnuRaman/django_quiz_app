from django import template

from ..models import Answer

register = template.Library()


@register.simple_tag
def has_student_completed_quiz(student, quiz):

    # Return a boolean signifying whether a user `student` has completed the questions
    # associated with `quiz`.

    useranswer_count = Answer.objects.filter(
        user_id=student.pk,
        question__in=quiz.questions.all()
    ).count()
    return bool(useranswer_count)
