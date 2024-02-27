
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializer import CreateQuestionSerializer
from drf_yasg.utils import swagger_auto_schema
from .schemas import *
from rest_framework.generics import ListAPIView
from ..models import QuizQuestions, QuizAnswers
from .serializer import GETAllQuizQuestionsSerializer
from django.db.models import Prefetch


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

    def get(self, request, quizId, *args, **kwargs):
        queryset = QuizQuestions.objects.select_related('quiz_id').prefetch_related(
            Prefetch('answers', queryset=QuizAnswers.objects.filter(isActive=True))
        ).filter(quiz_id=quizId, isActive=True)
        serializer = GETAllQuizQuestionsSerializer(queryset, many=True)

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

