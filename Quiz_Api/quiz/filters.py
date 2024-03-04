
import django_filters
from django.db.models import Q

from ..models import Quiz


class QuizFilter(django_filters.FilterSet):
    organization = django_filters.CharFilter(method='filter_organization')

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
            'totalQuestions': ['exact', 'gte', 'lte'],
            'order': ['exact', 'gte', 'lte'],
            'organization_id': ['exact'],
            'isVerified': ['exact'],
            'isActive': ['exact']
        }

    def filter_organization(self, queryset, name, value):
        if value.lower() == 'null':
            return queryset.filter(organization__isnull=True)
        return queryset.filter(organization=value)


class QuizCountFilter(django_filters.FilterSet):
    isAdmin = django_filters.BooleanFilter(method="filter_admin_quiz_count")
    # todayDate = django_filters.DateFilter()

    def filter_admin_quiz_count(self, queryset, name, value):
        if value:
            return queryset.filter(isActive=True, isVerified=True)
        elif not value:
            return queryset.filter(Q(isActive=False) | Q(isVerified=False))

        return queryset.filter(organization=value)
