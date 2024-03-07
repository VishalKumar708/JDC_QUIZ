
from rest_framework.views import APIView
from rest_framework.response import Response

from drf_yasg.utils import swagger_auto_schema
from .schemas import *
from ..models import QuizQuestions, QuizOptions
from .serializers.get import GETAllQuizQuestionsSerializer
from .serializers.create import CreateQuestionSerializer, CREATEOptionSerializer
from .serializers.update import UPDATEQuestionSerializer, UPDATEOptionSerializer

from django.db.models import Prefetch
from utils.utils import convert_str_to_bool
import logging
error_logger = logging.getLogger('error')
info_logger = logging.getLogger('info')
warning_logger = logging.getLogger('warning')


class POSTQuestions(APIView):
    message = "Record Added Successfully."
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
            info_logger.info("Question and options are added successfully.")
            return Response(data={
                'status': 'Success',
                'data': {"message": self.message, "question_id": data.id}
            })
        warning_logger.warning("Error occured while creating questions.")
        return Response(data={
            'status': 'Failed',
            'data': serializer.errors
        }, status=400)


class GETAllQuestionsByQuizId(APIView):

    def filter_queryset(self, request, quizId):
        options_isActive = request.GET.get('options__isActive')
        questions_isActive = request.GET.get('questions__isActive')
        try:
            options_isActive = convert_str_to_bool(options_isActive)
        except Exception:
            error_logger.error(f'str(e)')
            options_isActive =None

        try:
            questions_isActive = convert_str_to_bool(questions_isActive)
        except Exception as e:
            error_logger.error(f'str(e)')
            questions_isActive = None
        # print("option id=> ", options_isActive)
        # print("question => ", questions_isActive)
        if options_isActive is not None and questions_isActive is not None:
            return QuizQuestions.objects.select_related('quiz_id').prefetch_related(
                Prefetch('options', queryset=QuizOptions.objects.filter(isActive=options_isActive))
            ).filter(quiz_id=quizId, isActive=questions_isActive)
        elif options_isActive is not None:
            return QuizQuestions.objects.select_related('quiz_id').prefetch_related(
                Prefetch('options', queryset=QuizOptions.objects.filter(isActive=options_isActive))
            ).filter(quiz_id=quizId)
        elif questions_isActive is not None:
            return QuizQuestions.objects.select_related('quiz_id').prefetch_related(
                Prefetch('options', queryset=QuizOptions.objects.all())
            ).filter(quiz_id=quizId, isActive=questions_isActive)
        else:
            return QuizQuestions.objects.select_related('quiz_id').prefetch_related(
                Prefetch('options', queryset=QuizOptions.objects.all())
            ).filter(quiz_id=quizId)

    @swagger_auto_schema(tags=['Question API'], manual_parameters=requested_data_for_question_schema, responses={200: get_question_response_schema})
    def get(self, request, quizId, *args, **kwargs):
        try:
            filter_queryset = self.filter_queryset(request=request, quizId=quizId)

            serializer = GETAllQuizQuestionsSerializer(filter_queryset, many=True)

            if len(serializer.data) < 1:
                info_logger.info("Not any question added yet inside this quiz.")
                return Response(
                    data={
                        'status': 'Success',
                        'data': {'message': "No Record Found."}
                    },
                    status=200
                )
            info_logger.info("Return all questions with option Successfully.")
            return Response(data={
                'status': 'Success',
                'data': serializer.data
            }, status=200)
        except ValueError:
            warning_logger.warning("Quiz Id type error.")
            return Response(data={
                'status': 'Failed',
                'data': {"message": f"Excepted a number but got '{quizId}'"}
            }, status=404)


class PUTQuestionById(APIView):
    @swagger_auto_schema(tags=['Question API'], request_body=UPDATEQuestionSerializer,
                         responses={200: put_question_response_schema}, manual_parameters=put_question_requested_data_schema)
    def put(self, request, questionId, *args, **kwargs):
        try:
            instance = QuizQuestions.objects.get(id=questionId)
            serializer = UPDATEQuestionSerializer(instance=instance, data=request.data, partial=True, context={"quiz_id":instance.quiz_id,"question_id":questionId})
            if serializer.is_valid():
                obj = serializer.save()
                info_logger.info("Question update successfully.")
                return Response(data={
                    'status': 'Success',
                    'data': {'message': f'Record Updated Successfully.', 'questionId': obj.id}
                }, status=200)
            warning_logger.warning("Some Error occured while updating Quiz Question.")
            return Response(data={
                'status': 'Failed',
                'data': serializer.errors
            }, status=400)
        except QuizQuestions.DoesNotExist:
            warning_logger.warning("Received Invalid QuestionId.")
            return Response(data={
                'status': 'Failed',
                'data': {"message": f"Invalid questionId."}
            }, status=404)
        except ValueError:
            warning_logger.warning("Received QuestionId has value error.")
            return Response(data={
                'status': 'Failed',
                'data': {"message": f"Excepted a number but got '{questionId}'."}
            }, status=404)


class PUTOption(APIView):

    @swagger_auto_schema(tags=['Question API'], request_body=UPDATEOptionSerializer,
                         responses={200: put_question_response_schema},
                         manual_parameters=requested_data_for_put_option_schema)
    def put(self, request, optionId, *args, **kwargs):
        try:
            instance = QuizOptions.objects.get(id=optionId)
            serializer = UPDATEOptionSerializer(instance=instance, data=request.data, partial=True,
                                                context={'question_id': instance.question_id, 'answer_id': optionId})

            if serializer.is_valid():
                serializer.save()
                info_logger.info("Option Updated Successfully.")
                return Response(data={
                    'status': 'Success',
                    'data': {'message': f'Record Updated Successfully.'}
                }, status=200)
            warning_logger.warning("While updating option some error occured.")
            return Response(data={
                'status': 'Failed',
                'data': serializer.errors
            }, status=400)
        except QuizOptions.DoesNotExist:
            warning_logger.warning("Received Invalid OptionId.")
            return Response(data={
                'status': 'Failed',
                'data': {"message": f"Invalid answerId."}
            }, status=404)
        except ValueError:
            warning_logger.warning("Received OptionId has value error.")
            return Response(data={
                'status': 'Failed',
                'data': {"message": f"Excepted a number but got '{optionId}'."}
            }, status=404)


class POSTOption(APIView):
    message = 'Record Added Successfully.'
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
                        example=message
                    ),
                    'option_id': openapi.Schema(type=openapi.TYPE_INTEGER, example=78),
                }
            )
        }
    )
    @swagger_auto_schema(tags=['Question API'], request_body=CREATEOptionSerializer, responses={200: success_response})
    def post(self, request, *args, **kwargs):
        serializer = CREATEOptionSerializer(data=request.data)

        if serializer.is_valid():
            instance = serializer.save()
            info_logger.info("New Option Added Successfully.")
            return Response(data={
                'status': 'Success',
                'data': {'message': self.message, "option_id":instance.id}
            }, status=200)
        warning_logger.warning("While adding new option some error occured.")
        return Response(data={
            'status': 'Failed',
            'data': serializer.errors
        }, status=400)
