from drf_yasg import openapi
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializer import CreateQuizPlaySerializer
from ..models import QuizEnrollment, QuizPlay, QuizQuestions

from drf_yasg.utils import swagger_auto_schema
import logging
error_logger = logging.getLogger('error')
info_logger = logging.getLogger('info')
warning_logger = logging.getLogger('warning')


class POSTQuizPlay(APIView):
    success_message = "Answer submitted successfully."
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
                    # 'user_id': openapi.Schema(type=openapi.TYPE_INTEGER, example=1),
                }
            )
        }
    )

    @swagger_auto_schema(request_body=CreateQuizPlaySerializer(), responses={200: success_response})
    def post(self, request, *args, **kwargs):
        serializer = CreateQuizPlaySerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            obj = serializer.save()
            info_logger.info('User played quiz successfully.')
            return Response({
                'status': 'Success',
                'data': {'message': self.success_message}
            })
        warning_logger.warning("Error occured while playing a quiz")
        return Response({
            'status': 'Failed',
            'data': serializer.errors
        })


class GETReadyPlayQuiz(APIView):
    success_message = "You are ready to play quiz."
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
                    # 'user_id': openapi.Schema(type=openapi.TYPE_INTEGER, example=1),
                }
            )
        }
    )

    @swagger_auto_schema(responses={200: success_response})
    def get(self, request, quizId, userId, *args, **kwargs):
        try:
            filtered_enrolled_data = QuizEnrollment.objects.filter(quiz_id=quizId, user_id=userId)
            print("filtered_enrolled_data=> ", filtered_enrolled_data)
            if len(filtered_enrolled_data) == 0:
                return Response({
                    'status': 'Failed',
                    'data': {'message': "You are not enrolled in this quiz."}
                }, status=404)
            else:
                user_answered_check = QuizPlay.objects.filter(quizId=quizId, userId=userId).count()
                print("user_answered_check=> ", user_answered_check)
                print("status==> ", filtered_enrolled_data[0].status)
                if user_answered_check == 0:
                    total_number_of_questions = QuizQuestions.objects.filter(quiz_id=quizId, isActive=True).count()
                    print("total number of questions==> ", total_number_of_questions)
                    filtered_enrolled_data[0].pendingAnswer = total_number_of_questions
                    filtered_enrolled_data[0].status = 'start'
                    filtered_enrolled_data[0].save()
                    return Response({
                        'status': 'Success',
                        'data': {'message': self.success_message}
                    })
                elif filtered_enrolled_data[0].status.lower() in ['start'] and user_answered_check > 0:
                    return Response({
                        'status': 'Failed',
                        'data': {'message': "You are already playing quiz in another device."}
                    }, status=400)
                elif filtered_enrolled_data[0].status.lower() == 'complete' and user_answered_check > 0:
                    return Response({
                        'status': 'Failed',
                        'data': {'message': "You already Played this quiz."}
                    }, 400)
        except ValueError:
            return Response({
                'status': 'Failed',
                'data': {'message': "You are not enrolled in this quiz."}
            }, status=404)
