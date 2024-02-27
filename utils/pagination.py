from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class Pagination(PageNumberPagination):
    page_size_query_param = 'page_size'  # Name of the query parameter for page size
    max_page_size = 150  # Maximum number of records per page

    def get_paginated_response(self, data):
        return Response({**{
            "status": "Success",
            'count': self.page.paginator.count,
            'next': self.get_next_link(),
            'previous': self.get_previous_link(),

        }, **{'data': data}})  # Use 'data' instead of 'results'



