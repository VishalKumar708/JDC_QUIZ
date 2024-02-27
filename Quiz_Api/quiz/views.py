
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from .serializer import *
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from .schemas import *
from django_filters.rest_framework import DjangoFilterBackend
from .filters import QuizFilter
from utils.pagination import Pagination
from django.core.exceptions import FieldError


class POSTQuiz(APIView):

    message = "Record Added Successfully."

    # Define the response schema for success (200) response
    success_response = openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'data': openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'id': openapi.Schema(type=openapi.TYPE_INTEGER,  example=1),
                        'message': openapi.Schema(
                            type=openapi.TYPE_STRING,
                            # description=message,
                            example=message
                        )
                    }
                )
            }
        )

    @swagger_auto_schema(
        request_body=post_quiz_schema,
        responses={200: success_response},
        tags=['Quiz API']
    )
    def post(self, request, *args, **kwargs):
        serializer = CreateQuizSerializer(data=request.data)

        if serializer.is_valid():
            obj = serializer.save()
            return Response(data={
                "status": "Failed",
                'data': {
                    'id': obj.id,
                    'message': self.message
                }
            })
        return Response(data={
            "status": "Error",
            'data': serializer.errors}, status=400)


class PUTQuiz(APIView):
    message = 'Record Updated Successfully.'

    # Define the response schema for success (200) response
    success_response = openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'data': openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'message': openapi.Schema(
                        type=openapi.TYPE_STRING,
                        description=message,
                        example=message
                    )
                }
            )
        }
    )

    @swagger_auto_schema(
        tags=['Quiz API'],
        request_body=put_quiz_schema,
        responses={200: success_response},
        manual_parameters=[
            openapi.Parameter(
                name='id',
                in_=openapi.IN_PATH,
                type=openapi.TYPE_INTEGER,
                description="ID of the quiz (integer)"
            )
        ]
    )
    def put(self, request, id, *args, **kwargs):
        try:
            instance = Quiz.objects.get(id=id)
            serializer = UpdateQuizSerializer(instance, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response({
                    'status': 'Success',
                    'data': {'message': self.message}
                })
            return Response(data={
                "status": "Error",
                'data': serializer.errors
            }, status=400)
        except Quiz.DoesNotExist:
            return Response(data={
                "status": "Failed",
                'data': {'message': "Invalid Quiz Id."}
            }, status=404)
        except ValueError:
            return Response(data={
                "status": "Failed",
                'data': {'message': f"'quiz id' excepted a number but got '{id}'"}
            }, status=404)


class GETAllQuiz(ListAPIView):
    serializer_class = GETAllQuizSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = QuizFilter
    pagination_class = Pagination

    def get_queryset(self):
        queryset = Quiz.objects.all()
        order_by = self.request.query_params.get('order_by')
        if order_by:
            return queryset.order_by(order_by)

        return queryset.order_by('tittle')


    @swagger_auto_schema(
        tags=['Quiz API'],
        responses={
            200: openapi.Response('Successful response', get_response_schema),
            404: openapi.Response('No Record Found'),
        },
        pagination_class=Pagination,
        manual_parameters=[
            openapi.Parameter('page', openapi.IN_QUERY, description="Page number", type=openapi.TYPE_INTEGER),
            openapi.Parameter('page_size', openapi.IN_QUERY, description="Number of results per page",
                              type=openapi.TYPE_INTEGER),
            openapi.Parameter('order_by', openapi.IN_QUERY, description="Field to order by", type=openapi.TYPE_STRING),
        ]
    )
    def get(self, request, *args, **kwargs):
        try:
            queryset = self.filter_queryset(self.get_queryset())
        except FieldError:
            return Response(data={
                "status": "Error",
                "data": {"message": f"Invalid field name '{self.request.query_params.get('order_by')}' specified in "
                                    f"'order_by' parameter"}
            }, status=404)

        if queryset.exists():
            page = self.paginate_queryset(queryset)  # Perform pagination
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        else:
            return Response(data={
                "status": "Failed",
                "data": {
                    "message": "No Record Found"}
            }, status=404)


from django.db.models import Q, Case, When, IntegerField, Sum, Value
from django.db.models.functions import Coalesce
from datetime import datetime


class GETQuizCount(APIView):

    def get_queryset(self):
        today = datetime.today().date()
        print("today date==> ", today)
        return (
            Quiz.objects.filter(Q(isActive=True) & Q(isVerified=True))
            .aggregate(
                total_quiz_count=Coalesce(Sum(Case(When(Q(pk__isnull=False), then=1), output_field=IntegerField())),
                                          Value(0)),
                active_quiz_count=Coalesce(Sum(Case(When(Q(startDate__gte=today, endDate__lte=today), then=1), output_field=IntegerField())),
                                           Value(0)),
                past_quiz_count=Coalesce(Sum(Case(When(Q(endDate__lt=today), then=1), output_field=IntegerField())),
                                         Value(0)),
                upcoming_quiz_count=Coalesce(
                    Sum(Case(When(Q(startDate__gt=today), then=1), output_field=IntegerField())), Value(0)),
                result_quiz_count=Coalesce(Sum(Case(When(Q(resultDate=today), then=1), output_field=IntegerField())),
                                           Value(0))
            )
        )

    @swagger_auto_schema(tags=['Quiz API'])
    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        print("queryset==> ", queryset)
        return Response(
            data={
                'total_quiz': queryset['total_quiz_count'],
                'active_quiz': queryset['active_quiz_count'],
                'past_quiz': queryset['past_quiz_count'],
                'upcoming_quiz': queryset['upcoming_quiz_count'],
                'result_quiz_count': queryset['result_quiz_count']
            }
        )

