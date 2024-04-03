from django.core.exceptions import FieldError
from drf_yasg import openapi
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializer import QuizEnrolmentSerializer, GETAllQuizEnrolmentSerializer
from rest_framework.generics import ListAPIView
from ..models import QuizEnrollment
from drf_yasg.utils import swagger_auto_schema
from django_filters.rest_framework import DjangoFilterBackend
from .filters import QuizEnrollmentFilter
from utils.pagination import Pagination
import logging

error_logger = logging.getLogger('error')
info_logger = logging.getLogger('info')
warning_logger = logging.getLogger('warning')


class POSTQuizEnrollment(APIView):
    description = """
        <p>This API registers a user for a quiz by providing the necessary data.</p>
    """
    success_message = "Enrolled Successfully."
    success_response = openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'status': openapi.Schema(type=openapi.TYPE_STRING, example="Success"),
            'data': openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'message': openapi.Schema(
                        type=openapi.TYPE_STRING,
                        # description=message,
                        example=success_message
                    ),
                    'user_id': openapi.Schema(type=openapi.TYPE_INTEGER, example=1),
                }
            )
        }
    )

    @swagger_auto_schema(
        tags=["Quiz Enrollment And Play APIs"],
        request_body=QuizEnrolmentSerializer(),
        responses={200: success_response})
    def post(self, request, *args, **kwargs):
        serializer = QuizEnrolmentSerializer(data=request.data)
        if serializer.is_valid():
            obj = serializer.save()
            info_logger.info('User Enrolled Successfully in a Quiz.')
            return Response({
                'status': 'Success',
                'data': {'message': self.success_message, "user_id": obj.id}
            })
        warning_logger.warning("Error occured while enroll in a quiz")
        return Response({
            'status': 'Failed',
            'data': serializer.errors
        })


class GETAllQuizResult(ListAPIView):
    description = (
        """
        <p>This quiz API <strong>grants access</strong> to <strong>registered users</strong> and their associated quizzes, along with the <strong>results</strong> of their quiz <strong>participation</strong>.</p>
<p><br>Additionally, users have the capability to <strong>apply filters</strong> to <em>refine</em> the retrieved records according to their specific <em>requirements</em>.</p>
        """
    )

    serializer_class = GETAllQuizEnrolmentSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = QuizEnrollmentFilter
    pagination_class = Pagination

    def get_queryset(self):
        queryset = QuizEnrollment.objects.all()
        order_by = self.request.query_params.get('order_by')
        if order_by:
            return queryset.order_by(order_by)
        return queryset.order_by('enrollmentDate')

    @swagger_auto_schema(
        tags=['Quiz APIs'],
        # responses={
        #     200: openapi.Response('Successful response', get_response_schema),
        #     404: openapi.Response('No Record Found'),
        # },
        pagination_class=Pagination,
        manual_parameters=[
            openapi.Parameter('page', openapi.IN_QUERY, description="Page number", type=openapi.TYPE_INTEGER),
            openapi.Parameter('page_size', openapi.IN_QUERY, description="Number of results per page",
                              type=openapi.TYPE_INTEGER),
            # openapi.Parameter('order_by', openapi.IN_QUERY, description="Enter a valid field name to display the sorted results based on the specified field.", type=openapi.TYPE_STRING),
        ]
    )
    def get(self, request, *args, **kwargs):
        client_timezone = request.headers
        # print('client timezone=> ', client_timezone)
        try:
            queryset = self.filter_queryset(self.get_queryset())
        except FieldError:
            warning_logger.warning(f"Invalid field name({self.request.query_params.get('order_by')}) pass.")
            return Response(data={
                "status": "Failed",
                "data": {"message": f"Invalid field name '{self.request.query_params.get('order_by')}' specified in "
                                    f"'order_by' parameter"}
            }, status=404)

        if queryset.exists():
            page = self.paginate_queryset(queryset)  # Perform pagination
            # print("page==> ", page)
            serializer = self.get_serializer(page, many=True)
            info_logger.info("Record send Successfully.")
            return self.get_paginated_response(serializer.data)
        else:
            info_logger.info("No Record Found")
            return Response(data={
                "status": "Success",
                "data": {
                    "message": "No Record Found"}
            }, status=200)

