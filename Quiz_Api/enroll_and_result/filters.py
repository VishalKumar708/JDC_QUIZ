import django_filters
from django.db.models import Q

from ..models import QuizEnrollment
from django.db.models import Count


class QuizEnrollmentFilter(django_filters.FilterSet):
    # # organization = django_filters.CharFilter(method='filter_organization')
    # # show only those quiz where use is not enrolled
    # exclude_user_id = django_filters.NumberFilter(method='filter_exclude_user_id')
    # # total questions
    # totalQuestions_gte = django_filters.NumberFilter(method='filter_total_questions_gte')
    # totalQuestions_lte = django_filters.NumberFilter(method='filter_total_questions_lte')
    # totalQuestions = django_filters.NumberFilter(method='filter_total_questions')
    # # questions count for admin only
    # is_question_count_for_admin = django_filters.BooleanFilter(method='filter_question_count_for_admin')

    class Meta:
        model = QuizEnrollment
        fields = {
            'id': ['exact'],
            'user_id': ['exact'],
            'quiz_id': ['exact'],
            'status': ['exact']
            # 'title': ['exact', 'icontains'],
            # 'startDate': ['exact', 'gte', 'lte'],
            # 'endDate': ['exact', 'gte', 'lte'],
            # 'resultDate': ['exact', 'gte', 'lte'],
            # 'prize': ['exact', 'icontains'],
            # 'duration': ['exact', 'icontains'],
            # # 'totalQuestions': ['exact', 'gte', 'lte'],
            # 'order': ['exact', 'gte', 'lte'],
            # 'organization_id__name': ['icontains',],
            # 'isVerified': ['exact'],
            # 'isActive': ['exact'],
            # 'enrollments__user_id': ['exact']
        }
