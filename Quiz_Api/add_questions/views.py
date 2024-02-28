
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializer import CreateQuestionSerializer
from drf_yasg.utils import swagger_auto_schema
from .schemas import *
from ..models import QuizQuestions, QuizAnswers
from .serializer import GETAllQuizQuestionsSerializer
from django.db.models import Prefetch
from .filters import QuizQuestionsFilter
from utils.utils import convert_str_to_bool
from utils.pagination import Pagination

class POSTQuestions(APIView):
    message = "Record Added Successfully."
    success_response = openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'data': openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'message': openapi.Schema(
                        type=openapi.TYPE_STRING,
                        # description=message,
                        example=message
                    ),
                    'question_id': openapi.Schema(type=openapi.TYPE_INTEGER, example=1),
                }
            )
        }
    )

    @swagger_auto_schema(tags=['Question API'], request_body=post_question_schema, responses={200: success_response})
    def post(self, request, *args, **kwargs):
        print('question method call....')
        serializer = CreateQuestionSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.save()
            return Response(data={
                'status': 'Success',
                'data': {"message": self.message, "question_id": data.id}
            })
        return Response(data={
            'status': 'Failed',
            'data': serializer.errors
        }, status=400)


class GETAllQuestionsByQuizId(APIView):
    # pagination_class = Pagination # Define pagination class

    def filter_queryset(self, request, quizId):

        answers_isActive = request.GET.get('answers__isActive')
        questions_isActive = request.GET.get('questions__isActive')
        try:
            answers_isActive = convert_str_to_bool(answers_isActive)
        except Exception:
            answers_isActive =None

        try:
            questions_isActive = convert_str_to_bool(questions_isActive)
        except Exception:
            questions_isActive = None

        if answers_isActive is not None and questions_isActive is not None:
            return QuizQuestions.objects.select_related('quiz_id').prefetch_related(
                Prefetch('answers', queryset=QuizAnswers.objects.filter(isActive=answers_isActive))
            ).filter(quiz_id=quizId, isActive=questions_isActive)
        elif answers_isActive is not None:
            return QuizQuestions.objects.select_related('quiz_id').prefetch_related(
                Prefetch('answers', queryset=QuizAnswers.objects.filter(isActive=answers_isActive))
            ).filter(quiz_id=quizId)
        elif questions_isActive is not None:
            return QuizQuestions.objects.select_related('quiz_id').prefetch_related(
                Prefetch('answers', queryset=QuizAnswers.objects.all())
            ).filter(quiz_id=quizId, isActive=questions_isActive)
        else:
            return QuizQuestions.objects.select_related('quiz_id').prefetch_related(
                Prefetch('answers', queryset=QuizAnswers.objects.all())
            ).filter(quiz_id=quizId)

    @swagger_auto_schema(tags=['Question API'], manual_parameters=requested_data_for_question_schema, responses={200: get_question_response_schema})
    def get(self, request, quizId, *args, **kwargs):

        filter_queryset = self.filter_queryset(request=request, quizId=quizId)

        # Apply pagination
        # paginated_queryset = self.paginate_queryset(filter_queryset)
        # if paginated_queryset is not None:
        #     serializer = GETAllQuizQuestionsSerializer(paginated_queryset, many=True)
        #     return self.get_paginated_response(serializer.data)

        serializer = GETAllQuizQuestionsSerializer(filter_queryset, many=True)

        if len(serializer.data) < 1:
            return Response(
                data={
                    'status': 'Success',
                    'data': {'message': "No Record Found."}
                },
                status=200
            )

        return Response(data={
            'status': 'Success',
            'data': serializer.data
        }, status=200)
