
import django_filters
from ..models import Quiz


class QuizFilter(django_filters.FilterSet):
    organization = django_filters.CharFilter(method='filter_organization')

    class Meta:
        model = Quiz
        fields = {
            'id': ['exact'],
            'tittle': ['exact', 'icontains'],
            'startDate': ['exact', 'gte', 'lte'],
            'endDate': ['exact', 'gte', 'lte'],
            'resultDate': ['exact', 'gte', 'lte'],
            'prize': ['exact', 'icontains'],
            'duration': ['exact', 'icontains'],
            'totalQuestions': ['exact', 'gte', 'lte'],
            'order': ['exact', 'gte', 'lte'],
            'organization': ['exact'],
            'isVerified': ['exact'],
            'isActive': ['exact']
        }

    def filter_organization(self, queryset, name, value):
        if value.lower() == 'null':
            return queryset.filter(organization__isnull=True)
        return queryset.filter(organization=value)


# class QuizCountFilter(django_filters.FilterSet):
#     adminCount = django_filters.BooleanFilter(method="filter_admin_quiz_count")
#
#     def filter_admin_quiz_count(self, queryset, name, value):
#         if value.lower() == 'null':
#             return queryset.filter(organization__isnull=True)
#         return queryset.filter(organization=value)