from django_filters import rest_framework as filters
from ..models import QuizQuestions, QuizAnswers
from django.db.models import Exists, OuterRef, Prefetch


class QuizQuestionsFilter(filters.FilterSet):
    # questions__isActive = filters.BooleanFilter(method='filter_questions_is_active')
    # answers__isActive = filters.BooleanFilter(method='filter_answers_is_active')

    class Meta:
        model = QuizQuestions
        fields = {
            'level': ['iexact'],
            # 'answers__isActive': ['exact'],
            'isActive': ['exact'],
        }


    # def filter_answers_is_active(self, queryset, name, value):
    #     if value is not None:
    #         queryset = queryset.prefetch_related(
    #             Prefetch('answers', queryset=QuizOptions.objects.filter(isActive=value))
    #         )
    #
    #     return queryset

