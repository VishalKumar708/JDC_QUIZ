
import django_filters
from django.db.models import Q

from ..models import Quiz
from django.db.models import Count


class QuizFilter(django_filters.FilterSet):
    # organization = django_filters.CharFilter(method='filter_organization')
    # show only those quiz where use is not enrolled
    exclude_user_id = django_filters.NumberFilter(method='filter_exclude_user_id')
    # total questions
    totalQuestions_gte = django_filters.NumberFilter(method='filter_total_questions_gte')
    totalQuestions_lte = django_filters.NumberFilter(method='filter_total_questions_lte')
    totalQuestions = django_filters.NumberFilter(method='filter_total_questions')
    # questions count for admin only
    is_question_count_for_admin = django_filters.BooleanFilter(method='filter_question_count_for_admin')

    class Meta:
        model = Quiz
        fields = {
            'id': ['exact'],
            'title': ['exact', 'icontains'],
            'startDate': ['exact', 'gte', 'lte'],
            'endDate': ['exact', 'gte', 'lte'],
            'resultDate': ['exact', 'gte', 'lte'],
            'prize': ['exact', 'icontains'],
            'duration': ['exact', 'icontains'],
            # 'totalQuestions': ['exact', 'gte', 'lte'],
            'order': ['exact', 'gte', 'lte'],
            'organization_id__name': ['icontains',],
            'isVerified': ['exact'],
            'isActive': ['exact'],
            'enrollments__user_id': ['exact']
        }

    # def filter_organization(self, queryset, name, value):
    #     if value.lower() == 'null':
    #         return queryset.filter(organization__isnull=True)
    #     return queryset.filter(organization=value)

    def filter_exclude_user_id(self, queryset, name, value):
        if value:
            return queryset.exclude(enrollments__user_id=value)
        return queryset

    def filter_question_count_for_admin(self, queryset, name, value):
        # print("value=> ", value)
        if value is True:
            # Assuming YourModel has a foreign key named 'questions' pointing to Question model
            return queryset.annotate(totalQuestions=Count('quiz_questions__id'))

        return queryset

    # total_question methods
    def filter_total_questions_gte(self, queryset, name, value):
        if value:
            return queryset.annotate(totalQuestions=Count('quiz_questions__id')).filter(totalQuestions__gte=value)
        return queryset

    def filter_total_questions_lte(self, queryset, name, value):
        if value:
            return queryset.annotate(totalQuestions=Count('quiz_questions__id')).filter(totalQuestions__lte=value)
        return queryset

    def filter_total_questions(self, queryset, name, value):
        if value:
            return queryset.annotate(totalQuestions=Count('quiz_questions__id')).filter(totalQuestions=value)
        return queryset


class QuizCountFilter(django_filters.FilterSet):
    isAdmin = django_filters.BooleanFilter(method="filter_admin_quiz_count")
    # todayDate = django_filters.DateFilter()

    def filter_admin_quiz_count(self, queryset, name, value):
        if value:
            return queryset.filter(isActive=True, isVerified=True)
        elif not value:
            return queryset.filter(Q(isActive=False) | Q(isVerified=False))

        return queryset.filter(organization=value)
