import django_filters
from django.db.models import Q
from django.conf import settings
from django.db import models
from django import forms

from ..models import QuizEnrollment
from django.db.models import Count

date_format = getattr(settings, 'DEFAULT_DATE_FORMAT', "%d/%m/%Y")


class QuizEnrollmentFilter(django_filters.FilterSet):

    quiz_endDate__gt = django_filters.DateFilter(
        field_name='quiz_id__endDate',
        lookup_expr='gt',
        label="Show records where the end date of the associated quiz is after the specified date.",
        input_formats=[date_format])

    user_id = django_filters.NumberFilter(
        label="Filter will display all quizzes in which the specified user is enrolled.",
        help_text="Filter by the ID of the enrolled user."
    )
    quiz_id = django_filters.NumberFilter(
        label="Filter will display all users enrolled in the specified quiz.",
        help_text="Filter by the ID of the enrolled quiz.",

    )
    order_by = django_filters.CharFilter(
        method='filter_order_by',
        label="Enter a valid field name to display the sorted results based on the specified field."
        f"\nAvailable values: {[field.name for field in QuizEnrollment._meta.get_fields()]}"
        f"\n<br><i>If you provide only the value,the results will be displayed in 'ascending order'. "
        f"\nIf you provide the value prefixed with a minus sign (-),the results will be displayed in 'descending order'.</i>")

    status = django_filters.CharFilter(
        field_name='status',
        label=f"Display the user status indicating those who are currently enrolled, playing (incomplete), or have completed the quiz."
              f"\nPass multiple value with ',' separated <i>like '<b>enroll,start</b>'.</i>"
              f"\n<i>Available values: {[choice[0] for choice in QuizEnrollment.STATUS_CHOICES]}</i>",

        lookup_expr='in',
        method='filter_status'
    )

    attemptedQuiz_endDate__lte = django_filters.DateFilter(
        method='filter_quiz_endDate__lte',
        label="This filter will return results for all the quizzes you have completed or that have ended.",
        input_formats=[date_format])

    def filter_order_by(self, queryset, name, value):
        model_fields = [field.name for field in self.Meta.model._meta.get_fields()]
        if value in model_fields:
            return queryset.order_by(value)
        return queryset

    def filter_quiz_endDate__lte(self, queryset, name, value):
        if value:
            return queryset.filter(Q(quiz_id__endDate__lte=value) | Q(status='complete'))
        return queryset

    def filter_status(self, queryset, name, value):
        # print("actual value==> ", value)
        statuses = value.split(',')  # Split the comma-separated values into a list
        # print("status==> ", value)
        return queryset.filter(status__in=statuses)

    class Meta:
        model = QuizEnrollment
        fields = {
            'user_id': ['exact'],
            'quiz_id': ['exact'],
        }



