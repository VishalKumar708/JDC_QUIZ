from django_filters import rest_framework as filters
from ..models import QuizQuestions, QuizAnswers
from django.db.models import Exists, OuterRef, Prefetch


class QuizQuestionsFilter(filters.FilterSet):
    # questions__isActive = filters.BooleanFilter(method='filter_questions_is_active')
    answers__isActive = filters.BooleanFilter(method='filter_answers_is_active')

    class Meta:
        model = QuizQuestions
        fields = {
            'level': ['iexact'],
            # 'answers__isActive': ['exact'],
            'isActive': ['exact'],
        }

    # def filter_questions_is_active(self, queryset, name, value):
    #     print("question filter call.... ==> ", value)
    #     # print("queryset in filter method ==> ", queryset)
    #     # print("name is ==> ", name)
    #     if value is not None:
    #         # print("queryset==> ", queryset.filter(isActive=value))
    #         return queryset.filter(isActive=value)
    #
    #     print('queryset inside a filter==> ', queryset)
    #     return queryset

    # def filter_answers_is_active(self, queryset, name, value):
    #     print("answer filter call")
    #     print("value==> ", value)
    #     if value is not None:
    #         print("filter234 called ..")
    #         # print("filter query==> ", queryset.exclude(answers__isActive=value).query)
    #         # return queryset.filter(answers__isActive=value)
    #         # print("query==> ", queryset.filter(answers__isActive=value).distinct())
    #         return queryset.select_related('answers')
    #
    #     print("answer filter queryset==> ", queryset)
    #     return queryset

    def filter_answers_is_active(self, queryset, name, value):
        if value is not None:
            queryset = queryset.prefetch_related(
                Prefetch('answers', queryset=QuizAnswers.objects.filter(isActive=value))
            )

        return queryset

